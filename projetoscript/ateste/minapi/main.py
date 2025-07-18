from fastapi import FastAPI; app = FastAPI(); app.get("/")(lambda: {"id": 1})
