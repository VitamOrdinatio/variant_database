#!/usr/bin/env bash
set -u
set -o pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 -- <command...>" >&2
  exit 2
fi

if [[ "${1:-}" == "--" ]]; then
  shift
fi

RUN_TS="$(date -u +%Y_%m_%d_%H%M%S)"
RUN_ID="sys76_single_tep_vdb_baseline_${RUN_TS}"
RUN_DIR="results/validation/sys76_single_tep_baseline/${RUN_ID}"
LOG_DIR="${RUN_DIR}/logs"
METRICS_DIR="${RUN_DIR}/metrics"

mkdir -p "$LOG_DIR" "$METRICS_DIR"

COMMAND_STRING="$*"

{
  echo "run_id=${RUN_ID}"
  echo "start_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "hostname=$(hostname)"
  echo "pwd=$(pwd)"
  echo "git_commit=$(git rev-parse HEAD 2>/dev/null || echo unavailable)"
  echo "git_status_short_begin"
  git status --short 2>/dev/null || true
  echo "git_status_short_end"
  echo "command=${COMMAND_STRING}"
  echo
  echo "disk_before"
  df -h .
  echo
  echo "du_before_results"
  du -sh results 2>/dev/null || true
  echo
  echo "sqlite_files_before"
  find results -name "*.sqlite" -type f -printf "%p\t%s bytes\n" 2>/dev/null | sort || true
} | tee "${RUN_DIR}/run_context.log"

START_EPOCH="$(date +%s)"

# Run command with resource telemetry.
/usr/bin/time -v "$@" \
  > "${LOG_DIR}/stdout.log" \
  2> "${LOG_DIR}/stderr_time.log"

STATUS=$?
END_EPOCH="$(date +%s)"
ELAPSED_SECONDS="$((END_EPOCH - START_EPOCH))"

{
  echo "exit_code=${STATUS}"
  echo "end_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "elapsed_seconds=${ELAPSED_SECONDS}"
  echo
  echo "disk_after"
  df -h .
  echo
  echo "du_after_results"
  du -sh results 2>/dev/null || true
  echo
  echo "sqlite_files_after"
  find results -name "*.sqlite" -type f -printf "%p\t%s bytes\n" 2>/dev/null | sort || true
  echo
  echo "largest_outputs"
  find results -type f -printf "%s\t%p\n" 2>/dev/null | sort -nr | head -50 || true
} | tee "${RUN_DIR}/run_summary.log"

# SQLite metadata, best effort.
{
  echo "sqlite_metadata"
  while IFS= read -r db; do
    echo
    echo "sqlite_path=${db}"
    ls -lh "$db" || true
    if command -v sqlite3 >/dev/null 2>&1; then
      sqlite3 "$db" 'PRAGMA page_count;' 2>/dev/null | sed 's/^/page_count=/' || true
      sqlite3 "$db" 'PRAGMA page_size;' 2>/dev/null | sed 's/^/page_size=/' || true
      sqlite3 "$db" '.tables' 2>/dev/null | sed 's/^/tables=/' || true
    fi
  done < <(find results -name "*.sqlite" -type f 2>/dev/null | sort)
} | tee "${METRICS_DIR}/sqlite_metadata.log"

echo "telemetry_run_dir=${RUN_DIR}"

exit "${STATUS}"
