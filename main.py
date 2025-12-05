from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import uvicorn
import logging

from src.scheduler import lifespan
from database.requests import async_main, getUpdateInfo, getCours
from src.request_external_api import get_rates

app = FastAPI(
    title = 'CurrencyConversion',
    description= "API for working with currency exchange rates",
    root_path="/api/v1",
    lifespan=lifespan
)

logger = logging.getLogger(__name__)


@app.get('/update', tags = 'Update', description= "Update currency exchange rates in the database")
async def update() -> dict:
    try:
        await get_rates()
    except Exception as error:
        logger.error(f"Error updating rates: {error}")
        raise HTTPException(status_code=500, detail=str(error))
    else:
        return {
            "status": "success",
            "message": "Data successfully updated!"
        }

@app.get('/update/info', tags = 'Get info', description= "Get data about the latest database update")
async def updateInfo() -> dict:
    try:
        response = await getUpdateInfo()
    except Exception as error:
        logger.error(f"Error get update info: {error}")
        raise HTTPException(status_code=500, detail=str(error))
    else:
        return {
            'status' : 'success',
            'date_update' : response.date_update
        }
    
@app.get('/сonversion', tags = 'Conversion', description = "Conversion currency")
async def conversion(code_from: str, code_to: str, value: float) -> dict:
    cours_from = await get_currency_rate(code_from)
    cours_to = await get_currency_rate(code_to)

    return {
        code_from : cours_from,
        'value' : value,
        code_to : cours_to,
        'result_value' : cours_to * (1 / cours_from) * 100
    }


async def get_currency_rate(code):
    try:
        return await getCours(code)
    except AttributeError:
        raise HTTPException(status_code=404, detail=f'The currency {code} was not found!')

if __name__ == "__main__":
    asyncio.run(async_main())
    uvicorn.run('main:app', reload=True)