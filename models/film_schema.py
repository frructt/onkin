from pydantic import BaseModel


class Film(BaseModel):
    name: str
    genre: str
    year: int
