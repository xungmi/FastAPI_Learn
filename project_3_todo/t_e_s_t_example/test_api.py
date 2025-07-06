from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse

# Tạo app FastAPI ngay trong file test
app = FastAPI()

@app.get("/ping")
def ping():
    return JSONResponse(content={"message": "pong"}, status_code=200)

# Tạo TestClient cho app
client = TestClient(app)

def test_ping_endpoint():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}
