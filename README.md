# 🚀 JIRA Scrum Dashboard

Interaktywny dashboard do analizy wydajności zespołu Scrum z integracją JIRA API.

## ✨ Funkcje

- **📊 Live Data z JIRA** - pobiera dane w czasie rzeczywistym przez API
- **📈 Wykresy Interaktywne** - Chart.js dla wizualizacji danych
- **🏆 Rankingi Wydajności** - automatyczne rankingi zespołu
- **📉 Analiza Trendów** - śledzenie wydajności w czasie
- **⚡ Tryb Demo** - możliwość testowania bez API
- **🔄 Auto-refresh** - automatyczne odświeżanie danych
- **📱 Responsive Design** - działa na wszystkich urządzeniach

## 🛠️ Instalacja

### Opcja 1: Standalone HTML (Tryb Demo)

1. Otwórz plik `jira_dashboard.html` w przeglądarce
2. Kliknij "Tryb Demo" aby zobaczyć przykładowe dane
3. Nie wymaga instalacji!

### Opcja 2: Z Serwerem Proxy (Pełna integracja JIRA)

#### Wymagania:
- Python 3.7+
- pip

#### Instalacja:

```bash
# Zainstaluj zależności
pip install flask flask-cors requests

# Uruchom serwer proxy
python jira_proxy_server.py

# Serwer uruchomi się na http://localhost:5000
```

## 🔐 Konfiguracja JIRA

### 1. Utwórz API Token

1. Zaloguj się do JIRA/Atlassian
2. Idź do: https://id.atlassian.com/manage-profile/security/api-tokens
3. Kliknij "Create API token"
4. Nazwij token (np. "Dashboard")
5. Skopiuj wygenerowany token

### 2. Skonfiguruj Dashboard

W dashboardzie wypełnij:
- **JIRA URL**: `https://your-domain.atlassian.net`
- **Email**: Twój email użyty w JIRA
- **API Token**: Token wygenerowany w kroku 1
- **JQL Query**: np. `project = BESS ORDER BY updated DESC`

## 📊 Używanie Dashboard

### Podstawowe funkcje:

1. **Połączenie z JIRA**
   - Wypełnij dane konfiguracyjne
   - Kliknij "Połącz"
   - Status zmieni się na "Online"

2. **Metryki (górne karty)**
   - Total Story Points
   - Liczba zadań
   - Velocity średnie
   - Wielkość zespołu

3. **Porównanie Sprintów**
   - Automatyczne porównanie ostatnich 2 sprintów
   - Pokazuje zmiany procentowe

4. **Wykresy**
   - **Wydajność w Czasie**: Liniowy wykres pokazujący SP każdej osoby per sprint
   - **Sprint Velocity**: Słupkowy wykres velocity kolejnych sprintów

5. **Ranking Wydajności**
   - Top 3 osoby z największą ilością Story Points
   - Pokazuje średnią SP/zadanie

## 🔧 Zaawansowane opcje

### Custom JQL Queries

Przykłady przydatnych zapytań JQL:

```sql
-- Zadania z ostatnich 30 dni
project = BESS AND updated >= -30d

-- Tylko zakończone zadania
project = BESS AND status = Done

-- Zadania konkretnego użytkownika
project = BESS AND assignee = "John Doe"

-- Zadania z konkretnego sprintu
project = BESS AND sprint = "Sprint 19"

-- Zadania z Story Points
project = BESS AND "Story point estimate" > 0
```

### Modyfikacja Story Points Field

Jeśli Twoja JIRA używa innego pola dla Story Points:

1. Otwórz `jira_proxy_server.py`
2. Znajdź linię: `'storyPoints': fields.get('customfield_10016')`
3. Zmień `customfield_10016` na ID Twojego pola

Jak znaleźć ID pola:
- Idź do JIRA Settings → Custom Fields
- Znajdź pole Story Points
- ID będzie w URL lub opisie

## 🚨 Rozwiązywanie problemów

### Problem: CORS Error
**Rozwiązanie**: Użyj serwera proxy (`jira_proxy_server.py`)

### Problem: Authentication Failed
**Rozwiązanie**: 
- Sprawdź czy API token jest aktualny
- Upewnij się że używasz emaila (nie username)
- Sprawdź czy masz uprawnienia do projektu

### Problem: No Story Points
**Rozwiązanie**:
- Sprawdź ID pola Story Points w JIRA
- Zaktualizuj `customfield_10016` w kodzie

### Problem: Empty Sprint Name
**Rozwiązanie**:
- Niektóre zadania mogą nie mieć przypisanego sprintu
- Dashboard pokazuje je jako "No Sprint"

## 📝 Struktura plików

```
.
├── jira_dashboard.html      # Frontend dashboard
├── jira_proxy_server.py     # Backend proxy server
└── README.md               # Dokumentacja
```

## 🎨 Customizacja

### Zmiana kolorów wykresów

W `jira_dashboard.html` znajdź:
```javascript
const colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'];
```

### Zmiana liczby wyświetlanych zadań

Znajdź: `jiraData.slice(0, 10)` i zmień `10` na inną liczbę

### Dodanie nowych metryk

Dodaj nową kartę w sekcji metrics cards:
```html
<div class="metric-card text-white rounded-lg shadow p-6">
    <div class="flex justify-between items-center">
        <div>
            <p class="text-sm opacity-75">Nowa Metryka</p>
            <p class="text-3xl font-bold" id="newMetric">0</p>
        </div>
        <i class="fas fa-chart-pie text-3xl opacity-50"></i>
    </div>
</div>
```

## 🔄 Auto-refresh

Dashboard może automatycznie odświeżać dane:

```javascript
// Dodaj to do kodu JavaScript
setInterval(() => {
    if (document.getElementById('jiraToken').value) {
        refreshData();
    }
}, 300000); // Odśwież co 5 minut (300000ms)
```

## 📊 Export danych

Możesz dodać funkcję exportu do CSV:

```javascript
function exportToCSV() {
    const csv = jiraData.map(row => 
        `${row.key},${row.summary},${row.sprint},${row.assignee},${row.storyPoints}`
    ).join('\n');
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'jira_export.csv';
    a.click();
}
```

## 🔒 Bezpieczeństwo

⚠️ **WAŻNE**: 
- Nigdy nie commituj API tokenów do repozytorium
- Używaj zmiennych środowiskowych dla wrażliwych danych
- W produkcji używaj HTTPS
- Rozważ użycie OAuth 2.0 zamiast API tokenów

## 🤝 Wsparcie

Jeśli masz pytania lub problemy:
1. Sprawdź dokumentację JIRA API
2. Sprawdź logi w konsoli przeglądarki (F12)
3. Sprawdź logi serwera proxy

## 📜 Licencja

MIT License - używaj swobodnie!

## 🎯 Roadmap

Planowane funkcje:
- [ ] Eksport do PDF
- [ ] Więcej typów wykresów
- [ ] Predykcja velocity
- [ ] Integracja z Slack
- [ ] Dark mode
- [ ] Multi-projekt support
- [ ] Burndown charts
- [ ] Time tracking analysis

---

Made with ❤️ for Scrum Teams
