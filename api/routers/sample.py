"""Projects router"""

import logging
from enum import Enum



# from data_download_lib.lib.elastic import post_analyzed_to_elastic
from dotenv import load_dotenv
from fastapi import APIRouter, Query
from pydantic import BaseModel
from sqlmodel import func, select



load_dotenv()


logger = logging.getLogger("infinity-logger")
logger.setLevel(logging.INFO)
router = APIRouter()




@router.get("/dbconnection")
async def start():
    """dfdfdf"""

    return "posted_builders"


