from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware # 追加

from routers import auth, product, cart, order
import settings


app = FastAPI()
app.include_router(auth.router, prefix='/api')
app.include_router(product.router, prefix='/api')
app.include_router(cart.router, prefix='/api')
app.include_router(order.router, prefix='/api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"],       # 追記により追加
)


@app.get("/")
def hello() -> dict[str, str]:
    return {"message": "Hello, world"}
