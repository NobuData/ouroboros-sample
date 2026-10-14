#!/usr/bin/env sh
#
# file-issues.sh — file the ten demonstration issues from docs/issues/ on GitHub.
#
#   scripts/file-issues.sh [OWNER/REPO]
#
# Creates any label the issues use that the repository lacks, then files each issue in file
# order, so a fresh repository gets them as #1–#10. Needs `gh`, signed in to an account that
# can write issues. Run it once: it does not look for issues that already exist.

set -eu

repo=${1:-NobuData/ouroboros-sample}
cd "$(dirname "$0")/.."

field() { # field NAME FILE — a front-matter value
  sed -n "2,/^---$/s/^$1: //p" "$2"
}

for file in docs/issues/*.md; do
  field labels "$file" | tr -d '[]' | tr ',' '\n' | sed 's/^ *//; s/ *$//' | while read -r label; do
    [ -n "$label" ] || continue
    gh label create "$label" --repo "$repo" --force >/dev/null
  done
done

for file in docs/issues/*.md; do
  title=$(field title "$file" | sed 's/^"//; s/"$//')
  labels=$(field labels "$file" | tr -d '[]' | sed 's/, */,/g')
  body=$(awk 'n >= 2 { print } /^---$/ { n++ }' "$file")
  url=$(printf '%s\n' "$body" | gh issue create --repo "$repo" --title "$title" --label "$labels" --body-file -)
  printf '%s  %s\n' "$url" "$title"
done
