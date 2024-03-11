import os
import warnings
from typing import List

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

from search import vector_search

warnings.filterwarnings("ignore")

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, query: str = "") -> _TemplateResponse:
    result: List[str] = []
    if query:
        result = vector_search(query)
    return templates.TemplateResponse(
        "index.html", context={"request": request, "result": result, "query": query}
    )

if __name__ == "__main__":
    uvicorn.run(app)
