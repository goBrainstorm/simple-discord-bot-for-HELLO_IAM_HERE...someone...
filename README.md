# Discord-WhatsApp Voice Channel Bot

Ein Discord-Bot, der überwacht, wann Benutzer einem Voice Channel beitreten und nach einer bestimmten Zeit eine Nachricht in eine WhatsApp-Gruppe sendet.

## 🎯 Funktionsweise

1. **Discord Voice Monitoring**: Bot überwacht einen spezifischen Voice Channel
2. **Timer-System**: Startet einen Timer, wenn jemand dem Channel beitritt
3. **WhatsApp Integration**: Sendet nach Ablauf der Zeit eine Nachricht an eine WhatsApp-Gruppe
4. **Automatisierung**: Läuft vollautomatisch im Hintergrund

## 📋 Voraussetzungen

### Discord
- Discord Bot Application erstellt auf [Discord Developer Portal](https://discord.com/developers/applications)
- Bot Token
- Bot muss die `Voice States` Berechtigung haben
- Voice Channel ID des zu überwachenden Channels

### WhatsApp
**Option 1: PyWhatKit (Einfach, aber instabil)**
- WhatsApp Web muss im Browser eingeloggt sein
- Browser darf während der Ausführung nicht minimiert werden
- Funktioniert durch Automatisierung von WhatsApp Web

**Option 2: WhatsApp Business API (Empfohlen für Produktion)**
- WhatsApp Business Account
- Verifizierte Telefonnummer
- Meta Developer Account
- API-Schlüssel

## 🚀 Installation

1. **Repository klonen/herunterladen**

2. **Dependencies installieren**:
```bash
pip install -r requirements.txt
```

3. **Umgebungsvariablen konfigurieren**:
Erstelle eine `.env` Datei:
```env
DISCORD_TOKEN=dein_discord_bot_token
VOICE_CHANNEL_ID=123456789012345678
WHATSAPP_GROUP_ID=deine_whatsapp_gruppe_id
WAIT_TIME_MINUTES=1
```

4. **Bot starten**:
```bash
python discord_bot.py
```

## ⚙️ Konfiguration

### Discord Bot Setup
1. Gehe zu [Discord Developer Portal](https://discord.com/developers/applications)
2. Erstelle eine neue Application
3. Gehe zu "Bot" und erstelle einen Bot
4. Kopiere den Token
5. Aktiviere unter "Privileged Gateway Intents":
   - Server Members Intent
   - Message Content Intent

### Voice Channel ID finden
1. Aktiviere Developer Mode in Discord (User Settings → Advanced → Developer Mode)
2. Rechtsklick auf den gewünschten Voice Channel → "Copy ID"

### WhatsApp Gruppe ID finden (PyWhatKit)
1. Öffne WhatsApp Web
2. Öffne die gewünschte Gruppe
3. Die ID ist in der URL zu finden oder nutze Online-Tools

## 🔧 Bot-Befehle

- `!status` - Zeigt aktuell überwachte User im Voice Channel
- `!test_whatsapp [username]` - Testet WhatsApp-Nachricht (optional mit benutzerdefiniertem Namen)

## ⚠️ Wichtige Hinweise

### WhatsApp-Integration Limitierungen

**PyWhatKit Methode:**
- ❌ Instabil und fehleranfällig
- ❌ Benötigt offenen Browser
- ❌ Kann von WhatsApp erkannt und blockiert werden
- ✅ Einfach zu implementieren
- ✅ Kostenlos

**WhatsApp Business API:**
- ✅ Stabil und offiziell unterstützt
- ✅ Für Produktionsumgebungen geeignet
- ✅ Rate Limiting und Compliance
- ❌ Kostenpflichtig
- ❌ Komplexere Einrichtung

### Rechtliche Überlegungen
- Automatisierung von WhatsApp kann gegen die Nutzungsbedingungen verstoßen
- Für kommerzielle Nutzung sollte die WhatsApp Business API verwendet werden
- Benutzer sollten der Überwachung zustimmen

## 🛠️ Erweiterte Konfiguration

### Nachricht anpassen
In `config.py` kannst du das Nachrichtenformat ändern:
```python
MESSAGE_FORMAT = "{username} ist on 🎧"
```

### Wartezeit anpassen
Ändere `WAIT_TIME_MINUTES` in der `.env` Datei oder direkt in `config.py`.

### Mehrere Voice Channels überwachen
Erweitere die `voice_join_times` Logik um mehrere Channel IDs zu unterstützen.

## 🐛 Troubleshooting

### Discord Bot geht nicht online
- Überprüfe Bot Token
- Stelle sicher, dass der Bot auf dem Server ist
- Überprüfe Berechtigungen

### WhatsApp-Nachrichten werden nicht gesendet
- Stelle sicher, dass WhatsApp Web eingeloggt ist
- Überprüfe Gruppe ID
- Browser darf nicht minimiert sein (PyWhatKit)

### Voice Channel Events werden nicht erkannt
- Überprüfe Voice Channel ID
- Stelle sicher, dass Bot die `Voice States` Berechtigung hat
- Überprüfe Discord Intents

## 📝 Code-Struktur

```
discord_welcome_bot/
├── discord_bot.py          # Haupt-Bot-Datei
├── whatsapp_handler.py     # WhatsApp-Integration
├── config.py              # Konfiguration
├── requirements.txt       # Python-Dependencies
└── README.md             # Diese Datei
```

## 🔮 Mögliche Erweiterungen

- **Datenbank**: User-Aktivitäten persistent speichern
- **Web-Dashboard**: Status und Konfiguration über Web-Interface
- **Slack/Telegram Integration**: Alternative zu WhatsApp
- **Statistiken**: Tracking von Voice Channel Nutzung
- **Benachrichtigungs-Templates**: Verschiedene Nachrichten je nach Kontext
- **Multi-Server Support**: Bot auf mehreren Discord-Servern verwenden

## ⚖️ Haftungsausschluss

Dieses Projekt dient nur zu Demonstrationszwecken. Die Automatisierung von WhatsApp kann gegen die Nutzungsbedingungen verstoßen. Verwende es auf eigene Verantwortung und halte dich an alle geltenden Gesetze und Nutzungsbedingungen. 