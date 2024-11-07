# run api: fastapi dev main.py
# run vue: npm run serve

from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, or_

from fastapi.middleware.cors import CORSMiddleware

class ICDCode(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)
    description: str


# Database URL should ideally be in config or environment variables
DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=True)


def create_icd_codes(session: Session) -> None:
    icd_codes = [
        ICDCode(code="A00", description="Cholera"),
        ICDCode(code="A01", description="Typhoid and paratyphoid fevers"),
        ICDCode(code="A02", description="Other salmonella infections"),
    ]

    session.add_all(icd_codes)
    session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        create_icd_codes(session)

    yield

    SQLModel.metadata.drop_all(engine)


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all domains, adjust for security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

def get_session():
    with Session(engine) as session:
        yield session


@app.get("/icd_10_cm", response_model=List[ICDCode])
def read_icd_codes(
    *,
    session: Session = Depends(get_session),
    search: Optional[str] = Query(None, description="Search ICD codes and descriptions"),
):
    query = select(ICDCode)
    
    if search and search.strip():
        # Wrap the search term with wildcards for partial matching
        search_term = f"%{search.strip()}%"
        query = query.where(
            or_(
                ICDCode.code.ilike(search_term),  # Using ilike for case-insensitive search
                ICDCode.description.ilike(search_term)
            )
        )
    
    codes = session.exec(query).all()
    return codes