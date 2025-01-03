from fastapi import APIRouter, Query
from .scraper import fetch_oil_price
from typing import Optional
from fastapi.responses import JSONResponse

oilPrice = APIRouter()


@oilPrice.get("/api/oil-price", summary="获取油价")
async def get_oil_price(address: Optional[str] = Query(None, description="可选的地址")):
    if not address:
        # 使用 JSONResponse 来返回自定义格式
        return JSONResponse(
            status_code=400,
            content={"errorMsg": "请输入想要查询省份小写拼英地址"}
        )
    try:
        # 将地址传递给爬取函数，获取对应的油价数据
        price = fetch_oil_price(address)
        return {
            "status": "success",  # 标准化响应格式
            "data": {"today_oil_price": price}  # 将油价数据放入 data 字段
        }
    except Exception as e:
        # 异常情况的自定义错误信息
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "errorMsg": str(e)
            }
        )
