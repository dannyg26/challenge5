from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .settings import settings
from .db import engine, Base
from .routers import auth, transactions, investments, mortgage, budgets, dashboard

def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    Base.metadata.create_all(bind=engine)

    app.include_router(auth.router)
    app.include_router(transactions.router)
    app.include_router(investments.router)
    app.include_router(mortgage.router)
    app.include_router(budgets.router)
    app.include_router(dashboard.router)

    @app.get("/health")
    def health():
        return {"ok": True}

    return app

app = create_app()
