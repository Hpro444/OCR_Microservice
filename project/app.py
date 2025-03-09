import uvicorn
from fastapi import FastAPI
from project.routes.routes import router

app = FastAPI()

# Add the routes to the FastAPI app
app.include_router(router)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8067)
