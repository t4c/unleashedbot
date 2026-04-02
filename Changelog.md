# Changelog - Flipper Zero Release Bot

## [1.4.9] - 2026-04-02
- Patching-Logik im piratebuild.sh vereinfacht und Pfade neutralisiert.
- Bot-Ausgabe für ProtoPirate auf 'Changelog (Auszug)' vereinheitlicht.
- README.md um Konfigurationsanleitung für die Build-Bridge erweitert.


## [1.4.7] - 2026-03-29
- Globalen error_handler hinzugefügt.
- Abfanglogik für NetworkError (Bad Gateway) eingebaut.


## [1.4.6] - 2026-03-27
### Hinzugefügt
- Sync ProtoPirate Release mit version.json (als Changelog Ersatz)

## [1.2.0] - 2026-03-27
### Hinzugefügt
- **Intelligenter Momentum-Filter:** Zerlegt Changelogs in Sektionen (##) und entfernt automatisch Downloads, Support-Aufrufe und Spenden-Links (Ko-fi, PayPal, BTC).
- **Einheitliches Logging:** Jeder Befehl loggt nun Name, Username und die eindeutige Telegram-User-ID.
- **Link-Vorschau Deaktivierung:** Telegram-Web-Previews wurden global deaktiviert, um ein einheitliches Layout ohne störende Vorschaubilder zu erzwingen.

### Geändert
- **Code-Cleanup:** Überflüssige Kommentare und redundante Handler entfernt für maximale Übersichtlichkeit.
- **Text-Formatierung:** Markdown-Bereinigung optimiert (entfernt Symbole wie `>`, `#`, `**`), um die Lesbarkeit in Telegram-Codeblöcken zu verbessern.

---

## [1.1.0] - 2026-03-26
### Hinzugefügt
- **Asynchroner Kern:** Umstellung von `requests` auf `httpx`. Der Bot blockiert nun nicht mehr bei langsamen GitHub-Anfragen.
- **ARF-Support:** Befehl `/arf` für die Flipper-ARF Firmware hinzugefügt.
- **Visual Feedback:** Der Bot zeigt jetzt "tippt..." in Telegram an, während er die API-Daten abfragt.

---

## [1.0.1] - 2026-03-23
### Behoben
- **AttributeError (NoneType):** Absturz bei bearbeiteten Nachrichten durch Umstellung auf `effective_message` und `effective_chat` behoben.

---

## [1.0.0] - 2026-03-06
### Hinzugefügt
- **Initialer Release:** Basis-Bot für Flipper Zero Unofficial Germany.
- **Grundfunktionen:** Unterstützung für Momentum und Unleashed Firmware-Abfragen via GitHub API.
- **Zusatzbefehle:** `/protopirate`, `/uptime` und `/hilfe`.
- **Infrastruktur:** Docker-Support via `Dockerfile` und `docker-compose.yml`.
