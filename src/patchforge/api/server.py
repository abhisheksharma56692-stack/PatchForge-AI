"""FastAPI application factory and middleware configuration."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from patchforge.config import settings
from patchforge.api.routes.dashboard import router as dashboard_router
from patchforge.api.routes.vulnerabilities import router as vuln_router
from patchforge.api.routes.runs import router as runs_router
from patchforge.api.routes.pipeline import router as pipeline_router


def create_app() -> FastAPI:
    """Builds and configures the FastAPI application."""
    app = FastAPI(
        title="🎃 PatchForge AI Dashboard API",
        description="REST & WebSocket API backend for the Halloween-themed remediation console.",
        version="1.0.0",
    )

    # CORS configuration
    origins = [orig.strip() for orig in settings.dashboard_cors_origins.split(",") if orig.strip()]
    if "*" not in origins:
        origins.append("*")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount routes
    app.include_router(dashboard_router)
    app.include_router(vuln_router)
    app.include_router(runs_router)
    app.include_router(pipeline_router)

    @app.get("/api/health")
    def health():
        return {
            "status": "HEALTHY",
            "theme": "🎃 Halloween Dark Mode",
            "version": "1.0.0",
        }

    return app


app = create_app()

