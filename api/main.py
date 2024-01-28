"""Main app handler"""
import logging
import time
from logging.config import dictConfig
from os import environ


from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mangum import Mangum

from api import __version__

from api.routers import sample

load_dotenv()
# create_db_tables()

logging.basicConfig(filename='error.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')


DESCRIPTION = """
FASTAPI

"""

root_path: str = environ.get('ROOT_PATH')



app = FastAPI(
    root_path=root_path,
    version=__version__,
    description=DESCRIPTION,
    title="FASTAPI",
   
    redoc_url='/redoc'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """add process time"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response



# Builders route
app.include_router(prefix="/FASTAPI", router=sample.router)


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    """expection handler"""
    print(exc, request)
    return JSONResponse(
        status_code=400,
        content={"message": "Oops! There goes a rainbow...", "code": str(exc)},
    )

# for lambda handler
handler = Mangum(
    app=app,
    api_gateway_base_path=root_path
)