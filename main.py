from fastapi import FastAPI
import uvicorn
from apps.oilApp.urls import oilPrice

app = FastAPI()

app.include_router(oilPrice, prefix="/oilPrice", tags=["获取今日油价"])

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8080, debug=True, reload=True)
