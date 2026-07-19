# Workflow

Workflow (Orchestration):

1. Register TEP (TEP enters VDB) in sqlite

> For 1 TEP-VAP, see below for full run on ERR10619300

> The python command below registers just 2 TEP-GSCs

Run from VDB repo root:

```bash
python3 scripts/local/registration/run_sys76_double_gsc_registration.py \
  --overwrite
```



2. Validate registered sqlite

> Registering three TEPs (cross-repo): 1 TEP-VAP + 2 TEP-GSCs

Run from VDB repo root:

```bash
python3 scripts/local/validation/run_sys76_3tep_genotype_discovery_validation.py
```


# Canary Runs

Purpose: Run small batches of telemetry-equipped sqlite on sys76 (dev node) to extrapolate approximate time to completion for a full 1tep corpus (ERR10619300's TEP-VAP)

## Clean 1K Canary Calibration

```bash
cd /home/steelsparrow/dev/portfolio_projects/variant_database

source .venv/bin/activate

scripts/local/registration/run_single_tep_telemetry.sh -- \
  python3 scripts/local/registration/run_sys76_single_vap_registration.py \
    --tep "$TEP" \
    --db results/registration/sys76_single_ERR10619300_canary_idle_1k/vdb.sqlite \
    --producer-family VAP \
    --max-rows-per-artifact 1000 \
    --overwrite
```

---

## Clean 10K Canary Calibration

```bash
cd /home/steelsparrow/dev/portfolio_projects/variant_database

source .venv/bin/activate

scripts/local/registration/run_single_tep_telemetry.sh -- \
  python3 scripts/local/registration/run_sys76_single_vap_registration.py \
    --tep "$TEP" \
    --db results/registration/sys76_single_ERR10619300_calibration_idle_10k/vdb.sqlite \
    --producer-family VAP \
    --max-rows-per-artifact 10000 \
    --overwrite
```

### Get the 1K and 10K receipts

```bash
# Pointers to actual telemetry dirs printed by each canary run
RUN_1K="results/validation/sys76_single_tep_baseline/sys76_single_tep_vdb_baseline_2026_07_17_060948"
RUN_10K="results/validation/sys76_single_tep_baseline/sys76_single_tep_vdb_baseline_2026_07_17_061011"

echo "===== 1K stdout ====="
cat "$RUN_1K/logs/stdout.log"

echo "===== 1K time/resource ====="
cat "$RUN_1K/logs/stderr_time.log"

echo "===== 1K summary ====="
cat "$RUN_1K/run_summary.log"

echo "===== 10K stdout ====="
cat "$RUN_10K/logs/stdout.log"

echo "===== 10K time/resource ====="
cat "$RUN_10K/logs/stderr_time.log"

echo "===== 10K summary ====="
cat "$RUN_10K/run_summary.log"

echo "===== sqlite sizes ====="
find results/registration -maxdepth 2 -path '*ERR10619300*' -name 'vdb.sqlite' -printf '%p\t%s bytes\n' | sort
```

---

## Clean 10K Canary Calibration (Count Patched to Preserve Memory Usage)

```bash
scripts/local/registration/run_single_tep_telemetry.sh -- \
  python3 scripts/local/registration/run_sys76_single_vap_registration.py \
    --tep "$TEP" \
    --db results/registration/sys76_single_ERR10619300_calibration_idle_10k_countpatch/vdb.sqlite \
    --producer-family VAP \
    --max-rows-per-artifact 10000 \
    --overwrite
```

### Get 10K Canary Count-Patch Receipts

```bash
RUN_PATCHED_10K="results/validation/sys76_single_tep_baseline/sys76_single_tep_vdb_baseline_2026_07_17_064037"

cat "$RUN_PATCHED_10K/logs/stdout.log"
cat "$RUN_PATCHED_10K/logs/stderr_time.log"
cat "$RUN_PATCHED_10K/run_summary.log"
```


---

## Clean 30K Canary Calibration

```bash
tmux new-session -d -s vdb_err10619300_30k_calibration 'bash -lc "
set -euo pipefail

cd /home/steelsparrow/dev/portfolio_projects/variant_database
source .venv/bin/activate

TEP=/home/steelsparrow/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_07_14_114546/tep/vap_tep_ERR10619300_run_2026_07_14_114546_v1

test -d \"\$TEP\"

scripts/local/registration/run_single_tep_telemetry.sh -- \
  python3 scripts/local/registration/run_sys76_single_vap_registration.py \
    --tep \"\$TEP\" \
    --db results/registration/sys76_single_ERR10619300_calibration_idle_30k/vdb.sqlite \
    --producer-family VAP \
    --max-rows-per-artifact 30000 \
    --overwrite

echo
echo \"30k calibration finished. Press Ctrl-D or type exit to close this tmux shell.\"
exec bash
"'
```

---

### Watch the 30K Canary

```bash
watch -n 60 '
echo "=== time ==="
date

echo
echo "=== calibration sqlite ==="
ls -lh results/registration/sys76_single_ERR10619300_calibration_idle_30k/vdb.sqlite 2>/dev/null || true
du -sh results/registration/sys76_single_ERR10619300_calibration_idle_30k 2>/dev/null || true

echo
echo "=== disk ==="
df -h .

echo
echo "=== process ==="
ps -eo pid,etime,%cpu,%mem,rss,cmd | grep -E "run_sys76_single_vap_registration|python3" | grep -v grep || true
'
```

---

### Get the 30K Canary Receipts

```bash
find results/registration/sys76_single_ERR10619300_calibration_idle_30k -maxdepth 2 -type f -printf '%p\t%s bytes\n' | sort

RUN_DIR="PASTE_TELEMETRY_RUN_DIR_HERE"

cat "$RUN_DIR/logs/stdout.log"
cat "$RUN_DIR/logs/stderr_time.log"
cat "$RUN_DIR/run_summary.log"
```

---

# Feasibility Test

Purpose: Determine whether VDB can execute on sys76 (dev node)  

## Testing VDB Ingestion on sys76 on 1tep (ERR10619300)

SRA target = ERR10619300
TEP target = sys76-executed VAP-completed run of ERR10619300 (median read count, WES epilepsy cohort)

TEP=`/home/steelsparrow/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_07_14_114546/tep/vap_tep_ERR10619300_run_2026_07_14_114546_v1`


From VDB repo (4 steps):

### 1. Get a fresh pre-full (1tep run) snapshot

```bash
find "$TEP" -type f -printf "%p\t%T@\t%s\n" | sort > /tmp/tep_ERR10619300_before_full.tsv
```

---

### 2. Run TMUX on a single TEP-VAP

- Run is not `genotype-aware` yet
- Run is just testing whether / how long a VDB run takes on `sys76`

```bash
tmux new-session -d -s vdb_err10619300_sys76 'bash -lc "
set -euo pipefail

cd /home/steelsparrow/dev/portfolio_projects/variant_database
source .venv/bin/activate

TEP=/home/steelsparrow/dev/portfolio_projects/variant_annotation_pipeline/results/run_2026_07_14_114546/tep/vap_tep_ERR10619300_run_2026_07_14_114546_v1

test -d \"\$TEP\"

scripts/local/registration/run_single_tep_telemetry.sh -- \
  python3 scripts/local/registration/run_sys76_single_vap_registration.py \
    --tep \"\$TEP\" \
    --db results/registration/sys76_single_ERR10619300_current/vdb.sqlite \
    --producer-family VAP \
    --overwrite
"'
```

---

### 3. Watch in real-time

```bash
watch -n 60 '
date
du -sh results/registration/sys76_single_ERR10619300_current 2>/dev/null || true
ls -lh results/registration/sys76_single_ERR10619300_current/vdb.sqlite 2>/dev/null || true
df -h .
'
```

---

### 4. Capture a post-full snapshot of a 1tep run

```bash
find "$TEP" -type f -printf "%p\t%T@\t%s\n" | sort > /tmp/tep_ERR10619300_after_full.tsv

diff -u /tmp/tep_ERR10619300_before_full.tsv /tmp/tep_ERR10619300_after_full.tsv
```

```text
Should return no console out (meaning no differences pre-full and post-full VDB runs)
```

### 5. Capture Full Run 1tep Telemetry

```bash
RUN_FULL="$(ls -td results/validation/sys76_single_tep_baseline/sys76_single_tep_vdb_baseline_* | head -1)"

echo "RUN_FULL=$RUN_FULL"

echo "===== stdout ====="
cat "$RUN_FULL/logs/stdout.log"

echo "===== time/resource ====="
cat "$RUN_FULL/logs/stderr_time.log"

echo "===== summary ====="
cat "$RUN_FULL/run_summary.log"

echo "===== sqlite metadata ====="
cat "$RUN_FULL/metrics/sqlite_metadata.log"

echo "===== target sqlite size ====="
ls -lh results/registration/sys76_single_ERR10619300_current/vdb.sqlite
```

Focused SQLite count check:

```bash
sqlite3 results/registration/sys76_single_ERR10619300_current/vdb.sqlite '
SELECT "artifacts" AS table_name, COUNT(*) FROM artifacts
UNION ALL SELECT "assertion_registrations", COUNT(*) FROM assertion_registrations
UNION ALL SELECT "source_identities", COUNT(*) FROM source_identities
UNION ALL SELECT "package_metadata", COUNT(*) FROM package_metadata
UNION ALL SELECT "source_coordinate_declarations", COUNT(*) FROM source_coordinate_declarations
UNION ALL SELECT "source_feature_declarations", COUNT(*) FROM source_feature_declarations;
'
```

---

### Troubleshooting

#### Inspect Live `tmux` Sessions

```bash
tmux ls
```


#### Attach `tmux` 

```bash
tmux attach -t vdb_err10619300_sys76
```


#### Detach `tmux`

`Ctrl` + `B`
Let go of both keys (`Ctrl` + `B`)
Tap `D`


#### Kill `tmux`

```bash
tmux kill-session -t vdb_err10619300_sys76
```

