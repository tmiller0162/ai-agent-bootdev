#!/usr/bin/env zsh

set -euo pipefail

# Configuration
SANDBOX_USER="sandbox_user"

# Help message
function show_usage() {
  cat << EOF
Usage: $0 <workspace_dir> <script_rel_path> [script_args...]

Arguments:
  workspace_dir     Host directory the sandbox is allowed to access (read/write)
  script_rel_path   Path to the Python script relative to workspace_dir
  script_args       Optional arguments passed to the script

Example:
  $0 /srv/sandbox/allowed_dir script.py --verbose
EOF
  exit 1
}

# Require at least workspace_dir and script_rel_path
if [[ $# -lt 2 ]]; then
  show_usage
fi

WORKSPACE_DIR="$(realpath "$1")"
SCRIPT_PATH="$2"
shift 2

# Validation checks
if [[ ! -d "$WORKSPACE_DIR" ]]; then
  print -u2 "Error: Workspace directory does not exist: $WORKSPACE_DIR"
  exit 1
fi

if [[ ! -f "$WORKSPACE_DIR/$SCRIPT_PATH" ]]; then
  print -u2 "Error: Script does not exist inside workspace: $WORKSPACE_DIR/$SCRIPT_PATH"
  exit 1
fi

if ! id "$SANDBOX_USER" >/dev/null 2>&1; then
  print -u2 "Error: User '$SANDBOX_USER' does not exist."
  exit 1
fi

if ! command -v bwrap >/dev/null 2>&1; then
  print -u2 "Error: bubblewrap ('bwrap') is not installed."
  exit 1
fi

# Execute via sudo as the restricted user, applying bwrap containment
exec sudo -u "$SANDBOX_USER" -- bwrap \
  --ro-bind /usr /usr \
  --ro-bind /lib /lib \
  --ro-bind /lib64 /lib64 \
  --ro-bind /bin /bin \
  --proc /proc \
  --dev /dev \
  --bind "$WORKSPACE_DIR" /workspace \
  --chmod 500 /workspace \
  --chmod 700 /workspace/calculator \
  --chdir /workspace \
  --unshare-all \
  --die-with-parent \
  python3 "/workspace/$SCRIPT_PATH" "$@"
