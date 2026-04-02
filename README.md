# Flipper Zero Release Bot 🐬

Ein asynchroner, reaktiver Telegram-Bot, der die aktuellsten Firmware-Releases für den Flipper Zero direkt in deinen Chat liefert.

Dieser Bot wurde speziell für die Community von **[Flipper Zero Unofficial Germany](https://t.me/FlipperZeroUnofficialGermany)** entwickelt.

## 🚀 Funktionen
Der Bot reagiert auf folgende Befehle:

* `/momentum` – Aktuellstes Release der Momentum-Firmware (inkl. Sektions-Filter).
* `/unleashed` – Aktuellstes Release der Unleashed-Firmware.
* `/arf` – Aktuellstes Release der ARF-Firmware.
* `/protopirate` – Aktuelle ProtoPirate FAPs inklusive Changelog-Extraktion.
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

## 🏴‍☠️ Build Bridge (ProtoPirate)
Der Bot bezieht Informationen über ProtoPirate von einer öffentlichen JSON-URL. Um den Build und die Bridge zu automatisieren:

1. Nutze das mitgelieferte `piratebuild.sh` auf deinem Build-Server.
2. Passe die Variablen `USER_NAME`, `REPO_PATH` und `WEB_ROOT` im Script an.
3. Richte einen Cronjob ein (Beispiel für alle 6 Stunden):
   `0 */6 * * * /home/user/scripts/piratebuild.sh > /dev/null 2>&1`

Das Script erledigt das Kompilieren, Patchen der Emulation-Features und das Update der Bridge-Datei vollautomatisch.

---
*Entwickelt für Flipper Zero Unofficial Germany.*
