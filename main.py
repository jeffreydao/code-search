from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

class ICDCode(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(index=True)
    description: str

# Initialize FastAPI app
app = FastAPI()
engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

# Define test ICDCode records
icd_code_1 = ICDCode(code="A00", description="Cholera")
icd_code_2 = ICDCode(code="A01", description="Typhoid and paratyphoid fevers")
icd_code_3 = ICDCode(code="A02", description="Other salmonella infections")

# Insert records into the database
with Session(engine) as session:
    session.add(icd_code_1)
    session.add(icd_code_2)
    session.add(icd_code_3)
    session.commit()

with Session(engine) as session:
    statement = select(ICDCode).where(ICDCode.code == "A00")
    code_a00 = session.exec(statement).first()
    print(code_a00)