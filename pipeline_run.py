import subprocess
import sys
import logging
from datetime import datetime

logging.basicConfig(
    filename="pipeline_log.txt",
    level=logging.INFO,
    format="%(asctime)s — %(message)s"
)

def run_step(script_name):
    logging.info(f"Starting {script_name}...")
    print(f"Running {script_name}...")
    result = subprocess.run(
        [sys.executable, script_name],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        logging.info(f"{script_name} completed")
        logging.info(result.stdout)
        print(f"{script_name} done")
    else:
        logging.error(f"{script_name} failed")
        logging.error(result.stderr)
        raise Exception(f"{script_name} failed — check pipeline_log.txt")

if __name__ == "__main__":
    logging.info("=" * 50)
    logging.info(f"Pipeline started — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"\nPipeline started — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    try:
        run_step("useful_field.py")
        run_step("sql_implement.py")
        # run_step("skill_demand.py")
        print("\nFull pipeline completed successfully")
        logging.info("Full pipeline completed")
    except Exception as e:
        print(f"\nPipeline failed: {e}")
        logging.error(f"Pipeline stopped: {e}")

    logging.info("=" * 50)