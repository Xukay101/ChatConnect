from nanoid import generate
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True): # Refactorizar para que genere un id con nanoid
    # id: str = Field(primary_key=True)
    id: str = Field(default=lambda: generate(), primary_key=True)
