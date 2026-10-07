from fastapi import FastAPI
app = FastAPI(title="Transport Collection System",
              version= "1.0.0")

@app.get("/")
def home():
    return {
        "message" : "Transport Collection System "
    }