from typing import Annotated

from fastapi import Depends

from src.utils.unitofwork import IUnitOfWork, PgUnitOfWork

UOWDep = Annotated[IUnitOfWork, Depends(PgUnitOfWork)]
