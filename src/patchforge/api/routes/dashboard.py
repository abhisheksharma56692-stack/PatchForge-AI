"""Dashboard summary metrics endpoint."""
from fastapi import APIRouter
from patchforge.api.schemas import DashboardSummary

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardSummary)
def get_dashboard_summary():
    """Returns top-level overview metrics: skulls, bats, ghosts, cauldron health gauge."""
    return DashboardSummary(
        total_vulnerabilities=14,
        open_skulls=4,
        in_progress_bats=2,
        remediated_ghosts=8,
        mean_time_to_remediate_sec=172.0,
        pipeline_health_percent=98.8,
        active_runs=1,
    )

