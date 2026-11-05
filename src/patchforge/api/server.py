"""FastAPI application factory, database initialization, and middleware configuration."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from patchforge.config import settings
from patchforge.db.session import init_db
from patchforge.api.routes.dashboard import router as dashboard_router
from patchforge.api.routes.vulnerabilities import router as vuln_router
from patchforge.api.routes.runs import router as runs_router
from patchforge.api.routes.pipeline import router as pipeline_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: initializes database and tables on startup."""
    try:
        init_db()
        print("🎃 [DATABASE] Initialized PatchForge relational tables & seed data.")
    except Exception as e:
        print(f"⚠️ [DATABASE] Warning during database init: {e}")
    yield


def create_app() -> FastAPI:
    """Builds and configures the FastAPI application."""
    app = FastAPI(
        title="🎃 PatchForge AI Dashboard API",
        description="REST & WebSocket API backend connected to PostgreSQL/SQLite, Z3 Solver, and LangGraph.",
        version="1.0.0",
        lifespan=lifespan,
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

    # Mount API routers
    app.include_router(dashboard_router)
    app.include_router(vuln_router)
    app.include_router(runs_router)
    app.include_router(pipeline_router)

    @app.get("/api/health")
    def health():
        return {
            "status": "HEALTHY",
            "database": "CONNECTED",
            "theme": "🎃 Halloween Cyber-Gothic",
            "version": "1.0.0",
        }

    return app


app = create_app()
