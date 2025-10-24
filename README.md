# 🚀 JIRA Scrum Dashboard

An interactive dashboard for analyzing Scrum team performance with JIRA API integration.

[Polish version / Wersja polska](README.pl.md)

## ✨ Features

- **📊 Live JIRA Data** - real-time data fetching via API
- **🌐 Multi-language Support** - Polish and English (🇵🇱 🇬🇧)
- **🔄 Automatic Project Detection** - dynamically discovers all accessible JIRA projects
- **🎯 Smart Board Type Detection** - automatically detects Scrum vs Kanban boards
- **📈 Interactive Charts** - Chart.js visualizations
- **🏆 Performance Rankings** - automatic team rankings
- **📉 Trend Analysis** - track performance over time
- **📱 Responsive Design** - works on all devices
- **💾 Data Caching** - faster loading with intelligent caching
- **🔀 Flexible Views** - Sprint view for Scrum, Month view for Kanban

## 🛠️ Installation

### Requirements:
- Python 3.7+
- Modern web browser
- JIRA account with API access

### Quick Start:

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/jira-scrum-dashboard.git
cd jira-scrum-dashboard
```

2. **Install dependencies**
```bash
# On Linux/Mac:
chmod +x install.sh
./install.sh

# On Windows:
install.bat

# Or manually:
pip install -r requirements.txt
```

3. **Configure your credentials**
```bash
# Copy the example config
cp config.example.js config.js

# Edit config.js with your JIRA credentials
```

4. **Start the server**
```bash
# On Linux/Mac:
./start.sh

# On Windows/Manual:
python3 server.py

# Server will start at http://localhost:8000
```

5. **Open in browser**
```
http://localhost:8000/jira_dashboard.html
```

## 🔐 JIRA Configuration

### 1. Create API Token

1. Log in to JIRA/Atlassian
2. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
3. Click "Create API token"
4. Name it (e.g., "Dashboard")
5. Copy the generated token

### 2. Configure Dashboard

Fill in the dashboard form:
- **JIRA URL**: `https://your-domain.atlassian.net`
- **Email**: Your JIRA email
- **API Token**: Token from step 1
- **JQL Query**: Will be auto-generated per project

Or edit `config.js`:
```javascript
const CONFIG = {
    JIRA_URL: 'https://your-domain.atlassian.net',
    JIRA_EMAIL: 'your-email@example.com',
    JIRA_API_TOKEN: 'your-api-token',
    JQL_QUERY: 'project = "YOURPROJECT" ORDER BY updated DESC'
};
```

## 📊 Using the Dashboard

### Automatic Project Discovery

The dashboard automatically:
1. Fetches all accessible JIRA projects
2. Detects if each project uses Scrum or Kanban
3. Creates tabs for easy project switching
4. Adapts UI based on project type (disables sprint view for Kanban)

### Language Switching

Click the flag icons in the header:
- 🇵🇱 Polish
- 🇬🇧 English

Your language preference is saved automatically.

### Metrics Cards (Top Section)

- **Total Story Points** - sum of all story points
- **Tasks** - total number of issues with breakdown
- **Completion Rate** - percentage of completed tasks
- **Velocity** - average story points per sprint/month
- **In Progress** - current work in progress
- **Team** - team size and average SP per person

### Views

**Sprint View** (Scrum projects only):
- Shows data grouped by sprints
- Sprint velocity charts
- Sprint-based filters

**Month View** (All projects):
- Shows data grouped by months
- Monthly velocity trends
- Date range filters

### Charts

1. **Performance Over Time** - line chart showing each team member's story points per sprint/month
2. **Sprint/Month Velocity** - bar chart of total velocity
3. **Closed Issues by User** - stacked area chart
4. **Closed Issues Count** - task completion trends

### Filters

- **Sprint Filter** (Scrum): Last 1, 2, 3, 5, or 10 sprints
- **Date Range** (Month view): Various date ranges or custom dates
- **Status Filter**: All, Done, In Progress, To Do

## 🔧 Advanced Configuration

### Custom Story Points Field

If your JIRA uses a different Story Points field:

1. Find your field ID:
   - Go to JIRA issue view
   - Open browser dev tools (F12)
   - Look for the story points field in the API response

2. Update `jira_dashboard.html`:
```javascript
// Find this line (around line 1450):
storyPoints: sprintField?.[0]?.customfield_10016 || 0

// Replace customfield_10016 with your field ID
storyPoints: sprintField?.[0]?.customfield_XXXXX || 0
```

### Custom Sprint Field

Similarly for sprint field (usually `customfield_10020`):
```javascript
// Around line 1448:
sprintField = fields.customfield_10020;
```

## 🚨 Troubleshooting

### CORS Errors
**Solution**: Make sure you're using the included Python server (`server.py`). Don't open the HTML file directly.

### Authentication Failed
**Solution**:
- Verify your API token is current
- Use email address (not username)
- Check project permissions

### No Projects Showing
**Solution**:
- Verify you have access to at least one JIRA project
- Check browser console (F12) for error messages
- Clear cache: Click "Odśwież/Refresh" button

### Wrong Board Type Detected
**Solution**:
- The system checks actual sprint data
- If a "Scrum" board has no sprints, it's treated as Kanban
- Click refresh to re-detect board types

## 📁 Project Structure

```
.
├── jira_dashboard.html      # Main dashboard (frontend)
├── server.py                # Local server with CORS proxy
├── config.js                # Configuration (gitignored)
├── config.example.js        # Configuration template
├── install.sh               # Unix installation script
├── install.bat              # Windows installation script
├── start.sh                 # Unix startup script
├── requirements.txt         # Python dependencies
├── README.md               # Documentation (English)
├── README.pl.md            # Documentation (Polish)
└── .gitignore              # Git ignore rules
```

## 🎨 Customization

### Adding More Languages

Edit `jira_dashboard.html` and add to the `translations` object:

```javascript
const translations = {
    en: { /* English translations */ },
    pl: { /* Polish translations */ },
    es: { /* Spanish translations */ },
    // Add your language here
};
```

Then add a flag button in the header.

### Changing Chart Colors

Find the color definitions in `jira_dashboard.html`:
```javascript
backgroundColor: '#3B82F6',  // Blue
borderColor: '#2563EB',
```

## 🔒 Security

⚠️ **IMPORTANT**:
- Never commit API tokens to the repository
- `config.js` is gitignored by default
- Keep `.env` files private
- Use HTTPS in production
- Consider OAuth 2.0 for production deployments

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📜 License

MIT License - feel free to use!

## 🎯 Roadmap

Implemented:
- [x] Multi-language support (PL/EN)
- [x] Dynamic project detection
- [x] Scrum/Kanban auto-detection
- [x] Sprint/Month view switching
- [x] Data caching
- [x] Responsive design

Planned features:
- [ ] PDF export
- [ ] More chart types
- [ ] Velocity predictions
- [ ] Slack integration
- [ ] Dark mode
- [ ] Burndown charts
- [ ] Time tracking analysis
- [ ] More languages

## 📞 Support

If you have questions or issues:
1. Check the browser console (F12) for errors
2. Review JIRA API documentation
3. Open an issue on GitHub

---

Made with ❤️ for Scrum Teams
