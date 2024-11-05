## Phase 1: API

### Code
```python
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
```

## Overview:
1. Class `ICDCode` model represents the ICDCode table
2. We create the engine and setup our table
3. 3 ICD code records are defined and inserted
4. Those records are then added to the database
5. We find the code that matches A00 using `select(ICDCode).where(ICDCode.code == "A00")`