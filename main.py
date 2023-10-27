import logging
import string
import random
import time
from fastapi import FastAPI,Request,Depends
import uvicorn
from core import config,services
from db_models.models import Base
import logging
from fastapi.middleware.cors import CORSMiddleware
from api.routes import *
from api.routes import user, chat



logger = logging.getLogger()

Base.metadata.create_all(bind=config.get_engine_from_settings())


def get_application():
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(user.router)
    app.include_router(chat.router)

    return app


app = get_application()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response

@app.get("/")
async def root():
    logger.info("logging from the root logger")
    msg="hi"
    return {"status": "alive"}

@app.get("/api")
async def root_api():
    return {"Message":"Awsomme leads mmmanager"}
