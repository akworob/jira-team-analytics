#!/usr/bin/env python3
"""
JIRA API Proxy Server
Serwer proxy do komunikacji z JIRA API, który rozwiązuje problemy CORS
i umożliwia bezpieczne połączenie z frontendem.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64
import json
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)  # Włącz CORS dla wszystkich endpointów

# Cache dla danych (w produkcji użyj Redis)
cache = {}
CACHE_DURATION = 300  # 5 minut

@app.route('/api/connect', methods=['POST'])
def connect_jira():
    """Test połączenia z JIRA"""
    try:
        data = request.json
        jira_url = data.get('url')
        email = data.get('email')
        token = data.get('token')
        
        if not all([jira_url, email, token]):
            return jsonify({'error': 'Missing credentials'}), 400
        
        # Prepare auth header
        auth = base64.b64encode(f"{email}:{token}".encode()).decode()
        headers = {
            'Authorization': f'Basic {auth}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        # Test connection
        response = requests.get(
            f"{jira_url}/rest/api/3/myself",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            user_data = response.json()
            return jsonify({
                'success': True,
                'user': user_data.get('displayName', email)
            })
        else:
            return jsonify({'error': 'Authentication failed'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/issues', methods=['POST'])
def get_issues():
    """Pobierz zadania z JIRA"""
    try:
        data = request.json
        jira_url = data.get('url')
        email = data.get('email')
        token = data.get('token')
        jql = data.get('jql', 'ORDER BY updated DESC')
        
        # Check cache
        cache_key = f"{jira_url}:{jql}"
        if cache_key in cache:
            cached_data, cached_time = cache[cache_key]
            if datetime.now() - cached_time < timedelta(seconds=CACHE_DURATION):
                return jsonify(cached_data)
        
        # Prepare auth header
        auth = base64.b64encode(f"{email}:{token}".encode()).decode()
        headers = {
            'Authorization': f'Basic {auth}',
            'Accept': 'application/json'
        }
        
        # Build request
        params = {
            'jql': jql,
            'maxResults': 100,
            'fields': 'summary,status,assignee,customfield_10016,sprint,created,updated,priority,labels'
        }
        
        response = requests.get(
            f"{jira_url}/rest/api/3/search",
            headers=headers,
            params=params,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Process issues
            processed_issues = []
            for issue in data.get('issues', []):
                fields = issue.get('fields', {})
                
                # Get sprint info
                sprint_field = fields.get('sprint') or fields.get('customfield_10020')
                sprint_name = 'No Sprint'
                if sprint_field:
                    if isinstance(sprint_field, dict):
                        sprint_name = sprint_field.get('name', 'No Sprint')
                    elif isinstance(sprint_field, list) and sprint_field:
                        sprint_name = sprint_field[0].get('name', 'No Sprint')
                
                processed_issues.append({
                    'key': issue.get('key'),
                    'summary': fields.get('summary'),
                    'status': fields.get('status', {}).get('name'),
                    'assignee': fields.get('assignee', {}).get('displayName') if fields.get('assignee') else 'Unassigned',
                    'storyPoints': fields.get('customfield_10016') or fields.get('customfield_10014') or 0,
                    'sprint': sprint_name,
                    'created': fields.get('created'),
                    'updated': fields.get('updated'),
                    'priority': fields.get('priority', {}).get('name') if fields.get('priority') else 'None',
                    'labels': fields.get('labels', [])
                })
            
            result = {
                'issues': processed_issues,
                'total': data.get('total', len(processed_issues))
            }
            
            # Cache result
            cache[cache_key] = (result, datetime.now())
            
            return jsonify(result)
        else:
            return jsonify({'error': f'JIRA API error: {response.status_code}'}), response.status_code
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sprints', methods=['POST'])
def get_sprints():
    """Pobierz informacje o sprintach"""
    try:
        data = request.json
        jira_url = data.get('url')
        email = data.get('email')
        token = data.get('token')
        board_id = data.get('boardId', 1)  # Default board ID
        
        auth = base64.b64encode(f"{email}:{token}".encode()).decode()
        headers = {
            'Authorization': f'Basic {auth}',
            'Accept': 'application/json'
        }
        
        # Get sprints
        response = requests.get(
            f"{jira_url}/rest/agile/1.0/board/{board_id}/sprint",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            sprints_data = response.json()
            return jsonify(sprints_data)
        else:
            return jsonify({'error': f'Failed to get sprints: {response.status_code}'}), response.status_code
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/velocity', methods=['POST'])
def get_velocity():
    """Oblicz velocity dla ostatnich sprintów"""
    try:
        data = request.json
        issues = data.get('issues', [])
        
        # Group by sprint
        sprints = {}
        for issue in issues:
            sprint = issue.get('sprint', 'No Sprint')
            if sprint not in sprints:
                sprints[sprint] = {
                    'totalPoints': 0,
                    'completedPoints': 0,
                    'tasks': 0,
                    'completedTasks': 0,
                    'users': set()
                }
            
            points = issue.get('storyPoints', 0) or 0
            sprints[sprint]['tasks'] += 1
            sprints[sprint]['totalPoints'] += points
            
            if issue.get('assignee'):
                sprints[sprint]['users'].add(issue['assignee'])
            
            if issue.get('status') == 'Done':
                sprints[sprint]['completedTasks'] += 1
                sprints[sprint]['completedPoints'] += points
        
        # Convert to list and calculate metrics
        velocity_data = []
        for sprint_name, data in sprints.items():
            velocity_data.append({
                'sprint': sprint_name,
                'velocity': data['completedPoints'],
                'totalPoints': data['totalPoints'],
                'completedTasks': data['completedTasks'],
                'totalTasks': data['tasks'],
                'teamSize': len(data['users']),
                'completionRate': round((data['completedPoints'] / data['totalPoints'] * 100) if data['totalPoints'] > 0 else 0, 1)
            })
        
        # Sort by sprint name
        velocity_data.sort(key=lambda x: x['sprint'])
        
        # Calculate averages
        if velocity_data:
            avg_velocity = sum(s['velocity'] for s in velocity_data) / len(velocity_data)
            avg_completion = sum(s['completionRate'] for s in velocity_data) / len(velocity_data)
        else:
            avg_velocity = 0
            avg_completion = 0
        
        return jsonify({
            'sprints': velocity_data,
            'averageVelocity': round(avg_velocity, 1),
            'averageCompletion': round(avg_completion, 1)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics', methods=['POST'])
def get_analytics():
    """Zaawansowana analityka dla dashboard"""
    try:
        data = request.json
        issues = data.get('issues', [])
        
        # User statistics
        users = {}
        for issue in issues:
            assignee = issue.get('assignee', 'Unassigned')
            if assignee not in users:
                users[assignee] = {
                    'tasks': 0,
                    'storyPoints': 0,
                    'completedTasks': 0,
                    'completedPoints': 0,
                    'sprints': set()
                }
            
            points = issue.get('storyPoints', 0) or 0
            users[assignee]['tasks'] += 1
            users[assignee]['storyPoints'] += points
            users[assignee]['sprints'].add(issue.get('sprint', 'No Sprint'))
            
            if issue.get('status') == 'Done':
                users[assignee]['completedTasks'] += 1
                users[assignee]['completedPoints'] += points
        
        # Convert to list and calculate metrics
        user_analytics = []
        for name, data in users.items():
            user_analytics.append({
                'name': name,
                'tasks': data['tasks'],
                'storyPoints': data['storyPoints'],
                'completedTasks': data['completedTasks'],
                'completedPoints': data['completedPoints'],
                'averagePoints': round(data['storyPoints'] / data['tasks'] if data['tasks'] > 0 else 0, 1),
                'completionRate': round(data['completedPoints'] / data['storyPoints'] * 100 if data['storyPoints'] > 0 else 0, 1),
                'sprintsActive': len(data['sprints'])
            })
        
        # Sort by story points
        user_analytics.sort(key=lambda x: x['storyPoints'], reverse=True)
        
        # Status distribution
        status_dist = {}
        for issue in issues:
            status = issue.get('status', 'Unknown')
            status_dist[status] = status_dist.get(status, 0) + 1
        
        # Priority distribution
        priority_dist = {}
        for issue in issues:
            priority = issue.get('priority', 'None')
            priority_dist[priority] = priority_dist.get(priority, 0) + 1
        
        return jsonify({
            'users': user_analytics,
            'statusDistribution': status_dist,
            'priorityDistribution': priority_dist,
            'totalIssues': len(issues),
            'totalStoryPoints': sum(issue.get('storyPoints', 0) or 0 for issue in issues),
            'totalUsers': len(users),
            'uniqueSprints': len(set(issue.get('sprint', 'No Sprint') for issue in issues))
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 JIRA Proxy Server starting on port {port}")
    print(f"📊 Dashboard URL: http://localhost:{port}")
    print(f"🔗 API endpoints:")
    print(f"   - POST /api/connect - Test connection")
    print(f"   - POST /api/issues - Get issues")
    print(f"   - POST /api/sprints - Get sprints")
    print(f"   - POST /api/velocity - Calculate velocity")
    print(f"   - POST /api/analytics - Get analytics")
    
    app.run(host='0.0.0.0', port=port, debug=True)
