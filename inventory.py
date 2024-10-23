from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


@app.post("/on-order-created")
async def on_order_created(request: Request):
    try:
        order = await request.json()
    except Exception as e:
        return JSONResponse(
            content={"error": f"Invalid JSON: {str(e)}"}, status_code=400
        )

    return JSONResponse(content=order)


@app.post("/on-order-updated")
async def on_order_updated(request: Request):
    try:
        order = await request.json()
    except Exception as e:
        return JSONResponse(
            content={"error": f"Invalid JSON: {str(e)}"}, status_code=400
        )

    return JSONResponse(content=order)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("inventory:app", host="0.0.0.0", port=8000, reload=True)
