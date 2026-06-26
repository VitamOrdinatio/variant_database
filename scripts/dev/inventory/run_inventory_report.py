from pathlib import Path

from variant_database.ingestion.package_scanner import scan_package
from variant_database.ingestion.ingestion_reporter import write_inventory_reports

tep_path = Path(
    "/home/steelsparrow/dev/portfolio_projects/"
    "variant_annotation_pipeline/results/"
    "run_2026_06_03_010030/tep_emulation/"
    "vap_tep_HG002_run_2026_06_03_010030_v1_LIGHTWEIGHT_EMULATION"
)

inventory = scan_package(tep_path)

write_inventory_reports(
    inventory,
    Path("results/inventory_reports/hg002")
)

print("done")