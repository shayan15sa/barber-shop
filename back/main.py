from typing import Union, Annotated
from sqlmodel import Field, SQLModel, Relationship, Session, create_engine, select
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue default dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class Barber(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    age: int = Field(index=True)
    address: str = Field(index=True)

    hairstyles: list["Hairstyle"] = Relationship(back_populates="barber")
    examples: list["Example"] = Relationship(back_populates="barber")


class Hairstyle(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    likes: int = Field(default=0, index=True)
    barber_id: int | None = Field(default=None, foreign_key="barber.id")
    barber: Barber | None = Relationship(back_populates="hairstyles")

    examples: list["Example"] = Relationship(back_populates="hairstyle")


class Example(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    barber_id: int | None = Field(default=None, foreign_key="barber.id")
    hairstyle_id: int | None = Field(default=None, foreign_key="hairstyle.id")

    barber: Barber | None = Relationship(back_populates="examples")
    hairstyle: Hairstyle | None = Relationship(back_populates="examples")


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/barbers")
def create_barber(barber: Barber, session: SessionDep) -> Barber:
    session.add(barber)
    session.commit()
    session.refresh(barber)
    return barber


@app.get("/barbers")
def read_barbers(session: SessionDep) -> list[Barber]:
    barbers = session.exec(select(Barber).offset(0).limit(100)).all()
    return barbers


@app.post("/hairstyles")
def create_hairstyle(hairstyle: Hairstyle, session: SessionDep) -> Hairstyle:
    session.add(hairstyle)
    session.commit()
    session.refresh(hairstyle)
    return hairstyle


@app.get("/hairstyles", response_model=list[Hairstyle])
def read_hairstyles(session: SessionDep) -> list[Hairstyle]:
    statement = select(Hairstyle)
    hairstyles = session.exec(statement).all()
    return hairstyles


@app.get("/hairstyles/{hairstyle_id}", response_model=Hairstyle)
def read_hairstyle(hairstyle_id: int, session: SessionDep) -> Hairstyle:
    hairstyle = session.get(Hairstyle, hairstyle_id)
    if not hairstyle:
        raise HTTPException(status_code=404, detail="Hairstyle not found")
    return hairstyle


@app.put("/hairstyles/{hairstyle_id}", response_model=Hairstyle)
def update_hairstyle(
    hairstyle_id: int, hairstyle: Hairstyle, session: SessionDep
) -> Hairstyle:
    db_hairstyle = session.get(Hairstyle, hairstyle_id)
    if not db_hairstyle:
        raise HTTPException(status_code=404, detail="Hairstyle not found")

    db_hairstyle.name = hairstyle.name
    db_hairstyle.likes = hairstyle.likes
    db_hairstyle.barber_id = hairstyle.barber_id
    session.commit()
    session.refresh(db_hairstyle)
    return db_hairstyle


@app.delete("/hairstyles/{hairstyle_id}", response_model=Hairstyle)
def delete_hairstyle(hairstyle_id: int, session: SessionDep) -> Hairstyle:
    hairstyle = session.get(Hairstyle, hairstyle_id)
    if not hairstyle:
        raise HTTPException(status_code=404, detail="Hairstyle not found")

    session.delete(hairstyle)
    session.commit()
    return hairstyle


@app.post("/examples")
def create_example(example: Example, session: SessionDep) -> Example:
    session.add(example)
    session.commit()
    session.refresh(example)
    return example


@app.get("/examples", response_model=list[Example])
def read_examples(session: SessionDep) -> list[Example]:
    statement = select(Example)
    examples = session.exec(statement).all()
    return examples


@app.get("/examples/{example_id}", response_model=Example)
def read_example(example_id: int, session: SessionDep) -> Example:
    example = session.get(Example, example_id)
    if not example:
        raise HTTPException(status_code=404, detail="Example not found")
    return example


@app.put("/examples/{example_id}", response_model=Example)
def update_example(example_id: int, example: Example, session: SessionDep) -> Example:
    db_example = session.get(Example, example_id)
    if not db_example:
        raise HTTPException(status_code=404, detail="Example not found")

    db_example.barber_id = example.barber_id
    db_example.hairstyle_id = example.hairstyle_id
    session.commit()
    session.refresh(db_example)
    return db_example


@app.delete("/examples/{example_id}", response_model=Example)
def delete_example(example_id: int, session: SessionDep) -> Example:
    example = session.get(Example, example_id)
    if not example:
        raise HTTPException(status_code=404, detail="Example not found")

    session.delete(example)
    session.commit()
    return example


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
