#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: parse-headers.sh [OPTIONS] [FILE...]
Read input (or files) and print lines that look like HTTP headers:
HEADER-NAME: value
Options:
  -n, --names    Only print header names (text before the colon)
  -h, --help     Show this help and exit
Lines must start with a token (letters/digits/hyphen) followed immediately by a colon. Use '-' or no args to read stdin.
USAGE
}

# parse options
NAMES=0
while [[ "${1:-}" =~ ^- && "${1:-}" != "-" ]]; do
  case "$1" in
    -n|--names) NAMES=1; shift ;;
    -h|--help) usage; exit 0 ;;
    --) shift; break ;;
    *) echo "parse-headers.sh: unknown option '$1'" >&2; usage; exit 2 ;;
  esac
done

filter() {
  # Remove CR and print only lines that begin with token: (no leading space)
  if [[ "${NAMES:-0}" -eq 1 ]]; then
    # print the header name (text before the colon), trimmed, in lower case
    sed 's/\r$//' | awk '/^[A-Za-z0-9-]+:[ \t]*.*$/ { name=substr($0,1,index($0,":")-1); gsub(/[ \t]+$/,"",name); print name }' | tr '[:upper:]' '[:lower:]'
  else
    sed 's/\r$//' | awk '/^[A-Za-z0-9-]+:[ \t]*.*$/ { print }'
  fi
}

if [[ "$#" -eq 0 ]]; then
  filter
else
  for f in "$@"; do
    if [[ "$f" == "-" ]]; then
      filter
    else
      if [[ -r "$f" ]]; then
        filter < "$f"
      else
        echo "parse-headers.sh: cannot read '$f'" >&2
        exit 2
      fi
    fi
  done
fi
