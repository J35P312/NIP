"""Summarize the analysis"""

import logging
from pathlib import Path

from fluffy.slurm_api import SlurmAPI

LOG = logging.getLogger(__name__)


def get_summarize_cmd(
    singularity_exe: str, out_dir: Path, sample_sheet: str, zscore: str, mincnv: str
) -> str:
    """Return a string with the command to summarize a run"""
    outfile = out_dir / "summary.csv"
    summary_cmd = (
        f"singularity exec {singularity_exe} python /bin/FluFFyPipe/scripts/generate_csv.py "
        f"--folder {str(out_dir)} --samplesheet {sample_sheet} --Zscore {zscore} --minCNV {mincnv} "
        f"> {str(outfile)}"
    )
    return summary_cmd


def summarize_workflow(
    configs: dict, dependencies: list, slurm_api: SlurmAPI, dry_run: bool = False,
) -> int:
    """Run the workflow to summarize an analysis"""
    LOG.info("Run the summarize workflow")
    out_dir = configs["out"]

    summarize_cmd = get_summarize_cmd(
        singularity_exe=configs["singularity"],
        out_dir=out_dir,
        sample_sheet=configs["sample_sheet"],
        zscore=configs["summary"]["zscore"],
        mincnv=configs["summary"]["mincnv"],
    )

    jobid = slurm_api.run_job(
        name=f"summarize_batch",
        command=summarize_cmd,
        dependencies=dependencies,
        dry_run=dry_run,
    )

    return jobid