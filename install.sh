#!/bin/bash

echo "🚀 JIRA Dashboard Installer"
echo "=========================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 nie jest zainstalowany!"
    echo "Zainstaluj Python 3.7+ i spróbuj ponownie."
    exit 1
fi

echo "✅ Python znaleziony: $(python3 --version)"

# Create virtual environment
echo "📦 Tworzenie środowiska wirtualnego..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Aktywacja środowiska..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

# Install requirements
echo "📚 Instalacja zależności..."
pip install -r requirements.txt

echo ""
echo "✅ Instalacja zakończona!"
echo ""
echo "Aby uruchomić dashboard:"
echo "1. Aktywuj środowisko: source venv/bin/activate"
echo "2. Uruchom serwer: python jira_proxy_server.py"
echo "3. Otwórz przeglądarkę: http://localhost:5000"
echo "4. Lub otwórz bezpośrednio: jira_dashboard.html"
echo ""
echo "Miłej pracy! 🎉"
