from fastapi import FastAPI

from app.api import router

app = FastAPI(docs_url="/swagger")
app.include_router(router, prefix="/api")
