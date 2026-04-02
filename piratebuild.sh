#!/bin/bash
set -e

# --- KONFIGURATION ---
USER_NAME="user"
REPO_PATH="/home/$USER_NAME/repos/ProtoPirate"
WEB_ROOT="/var/www/ghcif.de/html/flipperzero"
# ---------------------

# Statischer Pfad für Cron-Stabilität ohne rekursive Variablen
export PATH=/home/$USER_NAME/.local/bin:/usr/local/bin:/usr/bin:/bin

cd "$REPO_PATH"
git fetch --all
git reset --hard origin/$(git rev-parse --abbrev-ref HEAD)
RELEASE=$(git describe --tags --always)

# Extrahiert den PR-Titel oder die erste Info-Zeile aus den Git-Logs
CHANGELOG=$(git log -1 --pretty=%B | \
    sed -E "s/^Merge (pull request|branch) '//; s/' (from|into) .*//" | \
    grep -vE "^(Reviewed-|Co-authored-by|Signed-off-by|http|Author:|Commit:)" | \
    grep -v "^$" | head -n 1 | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

echo "Patching files..."
sed -i 's/\/\/ #define ENABLE_EMULATE_FEATURE/#define ENABLE_EMULATE_FEATURE/g' defines.h
sed -i 's/gui/gui,subghz/g' application.fam

ufbt

# Bereitstellung der gebauten FAPs auf dem Webserver
cp dist/proto_pirate.fap "$WEB_ROOT/proto_pirate.fap"
cp dist/proto_pirate.fap "$WEB_ROOT/proto_pirate_${RELEASE}.fap"

# JSON Bridge für die Kommunikation mit dem Telegram Bot
echo "{\"version\": \"$RELEASE\", \"build_time\": \"$(date +'%d.%m.%Y um %H:%M')\", \"changelog\": \"$CHANGELOG\"}" > "$WEB_ROOT/version.json"

git reset --hard HEAD
