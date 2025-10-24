// Configuration loader for JIRA Dashboard
// Copy this file to config.js and add your credentials

const CONFIG = {
    JIRA_URL: 'https://your-domain.atlassian.net/',
    JIRA_EMAIL: 'your-email@example.com',
    JIRA_API_TOKEN: 'your-api-token-here',
    JQL_QUERY: 'project = "YOURPROJECT" ORDER BY updated DESC'
};

// Load configuration from localStorage if available
function loadConfig() {
    const savedToken = localStorage.getItem('jiraToken');
    if (savedToken) {
        CONFIG.JIRA_API_TOKEN = savedToken;
    }

    return CONFIG;
}

// Save API token to localStorage
function saveToken(token) {
    localStorage.setItem('jiraToken', token);
    CONFIG.JIRA_API_TOKEN = token;
}

// Initialize configuration on page load
function initConfig() {
    loadConfig();

    // Pre-fill form fields with configuration
    document.getElementById('jiraUrl').value = CONFIG.JIRA_URL;
    document.getElementById('jiraEmail').value = CONFIG.JIRA_EMAIL;
    document.getElementById('jqlQuery').value = CONFIG.JQL_QUERY;

    // Load saved token if exists
    const savedToken = localStorage.getItem('jiraToken');
    if (savedToken) {
        document.getElementById('jiraToken').value = savedToken;
    }
}
