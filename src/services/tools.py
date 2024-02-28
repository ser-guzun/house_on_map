import logging

from passlib.context import CryptContext


def validate_cadastral_number(number: str) -> bool:
    """АА:ВВ:ССССССС:КК"""

    number = number.split(sep=":")
    try:
        if len(number) != 4 or isinstance(int("".join(number)), int) is False:
            return False
        if (
            len(number[0]) != 2
            or len(number[1]) != 2
            or len(number[2]) != 7
            or len(number[3]) != 2
        ):
            return False
    except ValueError:
        logging.info(
            f"Elements of the cadastral number must contain only 'int'"
        )
        return False
