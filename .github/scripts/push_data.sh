#!/usr/bin/env bash
# Push result files to the orphan branch `wikitrends-data` under <label>/<run_id>/, preserving paths relative to wikitrends/.
# That branch's history never contains workflow files, so the GITHUB_TOKEN push is accepted
# (pushing a branch whose history adds workflow files is refused without the `workflows` permission).
# Usage: push_data.sh <label> <file-or-dir relative to $GITHUB_WORKSPACE/wikitrends>...
# Exits non-zero if the push fails after retries (never claims success it didn't get).
set -uo pipefail
LABEL="$1"; shift
SRC="$GITHUB_WORKSPACE/wikitrends"; DIR=/tmp/wt-data; DEST="$LABEL/${GITHUB_RUN_ID}"
URL="https://x-access-token:${GH_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
git config --global user.name "wikitrends-bot"; git config --global user.email "actions@users.noreply.github.com"
rm -rf "$DIR"
if git ls-remote --exit-code --heads origin wikitrends-data >/dev/null 2>&1; then
  git clone -q --depth 1 --branch wikitrends-data "$URL" "$DIR" || exit 1
else
  mkdir -p "$DIR" && cd "$DIR" && git init -q && git checkout -q -b wikitrends-data && git remote add origin "$URL"
fi
n=0
for p in "$@"; do
  for f in $(cd "$SRC" && ls -d $p 2>/dev/null); do
    mkdir -p "$DIR/$DEST/$(dirname "$f")" && cp -r "$SRC/$f" "$DIR/$DEST/$(dirname "$f")/" && n=$((n+1))
  done
done
echo "staged $n paths into $DEST"
[ "$n" -gt 0 ] || { echo "::error::no result files found to push"; exit 1; }
cd "$DIR" && git add -A && git commit -qm "data ${LABEL} ${GITHUB_RUN_ID} [skip ci]" || { echo "nothing new"; exit 0; }
for i in 1 2 3 4 5; do
  git pull -q --rebase origin wikitrends-data 2>/dev/null
  if git push -q origin HEAD:wikitrends-data; then echo "pushed $DEST to wikitrends-data"; exit 0; fi
  sleep $((i*5))
done
echo "::error::push to wikitrends-data failed after retries"; exit 1
