#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: redact-headers.sh [OPTIONS] [FILE...]
Read input (or files) and redact header values for a set of sensitive headers.
If no files are provided or a file is "-", read stdin.

Options:
  -l, --list    Print the header names that will be redacted and exit
  -h, --help    Show this help and exit

Example:
  redact-headers.sh raw/example.request > raw/example.redacted.request
USAGE
}

# headers that must be redacted (lowercase)
MUST_REDACT=(
  authorization
  chatgpt-account-id
  copilot-integration-id
  originator
  vscode-machineid
  vscode-sessionid
  x-request-id
  x-interaction-id
  x-initiator
)

# print list option
if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage; exit 0
fi
if [[ "${1:-}" == "-l" || "${1:-}" == "--list" ]]; then
  for h in "${MUST_REDACT[@]}"; do echo "$h"; done
  exit 0
fi

# produce a comma-separated list for awk
names=$(printf "%s," "${MUST_REDACT[@]}")
# remove trailing comma
names=${names%,}

redact_stream() {
  # remove CRs and run awk that redacts values for known headers (case-insensitive)
  sed 's/\r$//' | awk -v names="$names" '
    BEGIN {
      n = split(names, arr, ",");
      for (i=1;i<=n;i++) {
        redact[arr[i]] = 1
      }
    }
    # header line: token: value
    /^[A-Za-z0-9-]+:[ \t]*.*$/ {
      header = substr($0, 1, index($0, ":")-1)
      header_l = tolower(header)
      # preserve original header name casing, but replace value if in redact list
      if (redact[header_l]) {
        if (header_l == "authorization") placeholder = "<REDACTED TOKEN>"
        else placeholder = "<REDACTED ID>"
        print header ": " placeholder
      } else {
        print $0
      }
      next
    }
    { print }
  '
}

if [[ "$#" -eq 0 ]]; then
  redact_stream
else
  for f in "$@"; do
    if [[ "$f" == "-" ]]; then
      redact_stream
    else
      if [[ -r "$f" ]]; then
        redact_stream < "$f"
      else
        echo "redact-headers.sh: cannot read '$f'" >&2
        exit 2
      fi
    fi
  done
fi
