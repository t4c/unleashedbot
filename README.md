# Flipper Zero Release Bot 🐬

Ein asynchroner, reaktiver Telegram-Bot, der die aktuellsten Firmware-Releases für den Flipper Zero direkt in deinen Chat liefert.

Dieser Bot wurde speziell für die Community von **[Flipper Zero Unofficial Germany](https://t.me/FlipperZeroUnofficialGermany)** entwickelt.

## 🚀 Funktionen
Der Bot reagiert auf folgende Befehle:

* `/momentum` – Aktuellstes Release der Momentum-Firmware (inkl. Sektions-Filter).
* `/unleashed` – Aktuellstes Release der Unleashed-Firmware.
* `/arf` – Aktuellstes Release der ARF-Firmware.
* `/protopirate` – Link zu den Flipper Zero Tools (ghcif.de).
* `/uptime` – Zeigt die aktuelle Laufzeit des Bots.
* `/hilfe` – Übersicht aller verfügbaren Befehle.

## 📈 Projektstatus
Die gesamte Entwicklungshistorie und alle Neuerungen findest du im [Changelog](Changelog.md).

## 🛠 Installation & Setup
1. **Abhängigkeiten:** Der Bot nutzt `httpx` für asynchrone API-Abfragen.
2. **Umgebungsvariablen:** Erstelle eine `.env` Datei mit deinem Telegram-Token:
   ```env
   TelegramToken=DEIN_TOKEN_HIER
   ```
3. **Start mit Docker:**
   ```bash
   docker compose up -d --build
   ```

---
*Entwickelt für Flipper Zero Unofficial Germany.*
