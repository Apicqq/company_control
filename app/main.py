from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.api import router

app = FastAPI(docs_url="/swagger")
app.include_router(router, prefix="/api")
Instrumentator().instrument(app).expose(app)
