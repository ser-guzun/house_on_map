from typing import Annotated

from fastapi import Depends

from src.utils.unitofwork import IUnitOfWork, UserUnitOfWork

UOWDep = Annotated[IUnitOfWork, Depends(UserUnitOfWork)]
