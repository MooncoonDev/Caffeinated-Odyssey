# main.py
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse


fake_db = []


def get_application():
    app = FastAPI()

    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter


    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
        response = JSONResponse(
            {"error": f"Rate limit exceeded: {exc.detail}"},
            status_code=429
        )
        return _rate_limit_exceeded_handler(request, exc)


    class Coffee(BaseModel):
        name: str
        description: str
        price: float


    @app.post("/order")
    @limiter.limit("10/minute")
    async def create_order(request: Request, coffee: Coffee):
        order = {"id": len(fake_db) + 1, **coffee.dict()}
        fake_db.append(order)
        return {"id": order["id"], **coffee.dict()}  # Return the 'id' field in the response


    @app.get("/orders/{order_id}")
    async def get_order(order_id: int):
        for order in fake_db:
            if order["id"] == order_id:
                return order
        raise HTTPException(status_code=404, detail="Order not found")


    return app


app = get_application()
