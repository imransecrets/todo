from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select # type: ignore


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str = Field(index=True)
    

DATABASE_URL = f"postgresql://asif%20Imran:qxtpm01LNQEo@ep-shy-darkness-a7fy6bri-pooler.ap-southeast-2.aws.neon.tech/nexttodo?sslmode=require"


engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    create_db_and_tables()
    yield
    
   
app = FastAPI(lifespan=lifespan)


@app.post("/tasks/")

    
@app.put("/tasks/")
def update_tasks(task:Task):
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task.id)
        results = session.exec(statement)
        db_task = results.one()
        

        db_task.content = task.content
        session.add(db_task)
        session.refresh(db_task)
        return db_task

@app.get("/tasks/")
def read_tasks():
    with Session(engine) as session:
        task = session.exec(select(Task)).all()
        return task