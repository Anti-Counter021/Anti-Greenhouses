import typing

from sqlalchemy.orm import Session

from src.auth.domain import model


class VerificationRepository:
    """ Verification repository """

    def __init__(self, *, session: Session) -> None:
        self.session = session

    def add(self, *, verification: model.Verification) -> None:
        self.session.add(verification)

    def get(self, **filtration: str) -> typing.Optional[model.Verification]:
        return self.session.query(model.Verification).filter_by(**filtration).first()

    def remove(self, **filtration: str) -> None:
        self.session.query(model.Verification).filter_by(**filtration).delete()