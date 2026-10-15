#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 || ! -f "$1" ]]; then
  echo "Usage: $0 /path/to/owned-game.apk" >&2
  exit 2
fi

apk=$1
command -v unzip >/dev/null 2>&1 || { echo "Error: unzip is required" >&2; exit 1; }

echo "== Native libraries (ABI directories) =="
mapfile -t libs < <(unzip -Z1 "$apk" | grep -E '^lib/[^/]+/[^/]+\.so$' || true)
if ((${#libs[@]} == 0)); then
  echo "No packaged native .so libraries found (or APK is split/uses external assets)."
else
  printf '%s\n' "${libs[@]}"
  echo
  echo "ABI summary:"
  printf '%s\n' "${libs[@]}" | awk -F/ '{print $2}' | sort -u
fi

echo
echo "== Package metadata (if Android SDK tools are installed) =="
if command -v apkanalyzer >/dev/null 2>&1; then
  apkanalyzer manifest application-id "$apk" || true
  apkanalyzer manifest min-sdk "$apk" || true
  apkanalyzer manifest target-sdk "$apk" || true
elif command -v aapt >/dev/null 2>&1; then
  aapt dump badging "$apk" | grep -E "^(package:|sdkVersion:|targetSdkVersion:|native-code:)" || true
else
  echo "Install Android SDK command-line tools (apkanalyzer or aapt) for package/SDK metadata."
fi

echo
echo "Note: this inventory does not emulate or convert ARM32 code. It is a diagnostic first step."
