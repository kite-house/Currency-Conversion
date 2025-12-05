from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from contextlib import asynccontextmanager
from fastapi import FastAPI

from .request_external_api import get_rates

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        scheduler.add_job(
            get_rates,
            trigger=IntervalTrigger(minutes=1),
            id='currency_update_job',
            replace_existing=True
        )
        scheduler.start()
        yield
    except Exception:
        pass

    finally:
        scheduler.shutdown()















