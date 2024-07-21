from typing import Annotated

from fastapi import Depends

from src.dependencies.db_session import SessionMakerDep
from src.utils.unitofwork import PgUnitOfWork


def create_pg_uow(session_maker: SessionMakerDep):
    return PgUnitOfWork(session_maker=session_maker)


PgUnitOfWorkDep = Annotated[PgUnitOfWork, Depends(create_pg_uow)]
