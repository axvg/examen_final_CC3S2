from fastapi import FastAPI
import uvicorn

from microservice.api.routes import router as api_router
from microservice.services.database import init_db


def get_application() -> FastAPI:
    app = FastAPI(
        title="Microservicio todos ",
        description="Microservicio para lista todos",
        version="0.1.0",
        docs_url="/",
        redoc_url=None,
    )

    app.include_router(api_router)

    @app.on_event("startup")
    def on_startup() -> None:
        init_db()

    return app

app = get_application()


if __name__ == "__main__":
    uvicorn.run(
        "microservice.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
