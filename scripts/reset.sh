#!/usr/bin/env sh
#
# reset.sh — return the repository to where a demonstration run starts.
#
#   scripts/reset.sh [--restore-main] [OWNER/REPO]
#
# 1. Closes every open pull request whose branch starts with the run-branch prefix
#    (OURO_RUN_BRANCH_PREFIX, default "ouro/run-") and deletes those branches.
# 2. Reopens any of the ten demonstration issues that a run closed.
# 3. With --restore-main only: moves `main` back to the tag `demo-start`, which is where the
#    demonstration begins. This rewrites `main` on GitHub — it asks first.
#
# Comments a run left on issues stay: they are the record of what happened. Needs `gh`
# (signed in, with write access).

set -eu

restore_main=false
if [ "${1:-}" = --restore-main ]; then
  restore_main=true
  shift
fi
repo=${1:-NobuData/ouroboros-sample}
prefix=${OURO_RUN_BRANCH_PREFIX:-ouro/run-}

echo "Closing open pull requests from ${prefix}* branches in $repo"
gh pr list --repo "$repo" --state open --limit 200 --json number,headRefName \
  --jq ".[] | select(.headRefName | startswith(\"$prefix\")) | \"\(.number) \(.headRefName)\"" |
  while read -r number branch; do
    gh pr close "$number" --repo "$repo" --comment "Closed by scripts/reset.sh to repeat the demonstration." >/dev/null
    echo "  closed #$number ($branch)"
  done

echo "Deleting ${prefix}* branches"
gh api "repos/$repo/git/matching-refs/heads/$prefix" --jq '.[].ref' |
  while read -r ref; do
    gh api -X DELETE "repos/$repo/git/$ref" >/dev/null
    echo "  deleted ${ref#refs/heads/}"
  done

echo "Reopening closed demonstration issues"
cd "$(dirname "$0")/.."
for file in docs/issues/*.md; do
  title=$(sed -n '2,/^---$/s/^title: //p' "$file" | sed 's/^"//; s/"$//')
  gh issue list --repo "$repo" --state closed --search "in:title \"$title\"" --json number,title \
    --jq ".[] | select(.title == \"$title\") | .number" |
    while read -r number; do
      gh issue reopen "$number" --repo "$repo" >/dev/null
      echo "  reopened #$number"
    done
done

if [ "$restore_main" = true ]; then
  start=$(gh api "repos/$repo/git/ref/tags/demo-start" --jq .object.sha 2>/dev/null || true)
  [ -n "$start" ] || { echo "reset.sh: the repository has no tag demo-start" >&2; exit 1; }
  printf 'Move main on %s back to demo-start (%s)? This rewrites history. [y/N] ' "$repo" "$start"
  read -r answer
  case $answer in
    y | Y | yes) gh api -X PATCH "repos/$repo/git/refs/heads/main" -f sha="$start" -F force=true >/dev/null
                 echo "  main is at demo-start" ;;
    *) echo "  main left as it is" ;;
  esac
fi

echo "Done."
