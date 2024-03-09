from fastapi import FastAPI
from routers.img_async import router as async_router
from routers.img_sync import router as sync_router

app = FastAPI()

# Include the routers in the app
app.include_router(sync_router)
app.include_router(async_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
