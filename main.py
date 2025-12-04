from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title = 'CurrencyConversion',
    description= "API for working with currency exchange rates",
    root_path="/api/v1"
)


...




if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)