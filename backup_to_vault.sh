#!/bin/sh
# Copy the course site's source into the Obsidian vault, so whatever backs up the vault (Obsidian Sync) backs up the site too.
# Runs hourly from the spanish-site-backup systemd user timer; safe to run by hand.
set -eu
SITE="$HOME/Documents/Spanish/Site"
DEST="$HOME/Documents/Spanish/Spanish/Site Backup"
mkdir -p "$DEST/systemd"
rsync -a --delete --exclude .venv --exclude __pycache__ --exclude .git --exclude public --exclude 'README.md' "$SITE/" "$DEST/Site/"
cp "$HOME/.config/systemd/user/spanish-site.service" "$HOME/.config/systemd/user/spanish-site-backup.service" \
   "$HOME/.config/systemd/user/spanish-site-backup.timer" "$DEST/systemd/"
cat > "$DEST/README.md" <<EOF
# Site Backup
A copy of the course website (\`~/Documents/Spanish/Site\`), refreshed every hour. Last copied: $(date '+%Y-%m-%d %H:%M').
Don't edit files here — edit the real site; this folder is overwritten.

## Restore on a new machine
1. Copy \`Site/\` to \`~/Documents/Spanish/Site\` (next to this vault, which must be at \`~/Documents/Spanish/Spanish\`).
2. \`python3 ~/Documents/Spanish/Site/server.py\` → http://127.0.0.1:8765
3. Optional, to run it in the background: copy \`systemd/*\` to \`~/.config/systemd/user/\`, then
   \`systemctl --user enable --now spanish-site spanish-site-backup.timer\`, and \`tailscale serve --bg 8765\` for the tailnet link.
4. Photo/audio downloads need the venv: \`cd ~/Documents/Spanish/Site && python3 -m venv .venv\` and install what \`fetch_media.py\` imports.
EOF
