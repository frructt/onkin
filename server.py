from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

import db_interface
import parameters
import sql.films_table

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/films/")
def get_all_films():
    connection = db_interface.DatabaseInterface(parameters.server, parameters.database, parameters.uid, parameters.pwd)
    serialized_films = connection.db_to_dict(sql.films_table.get_all_films)
    if not serialized_films:
        raise HTTPException(
            status_code=404,
            detail="Films are not found",
            headers={"X-Error": "There goes my error"},
        )
    return serialized_films


# if __name__ == '__main__':
#     uvicorn.run(app)
