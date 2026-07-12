from sqlalchemy.orm import Session

from app.models.role import Role


class RoleRepository:

    @staticmethod
    def get_by_name(db: Session, name: str):

        return (
            db.query(Role)
            .filter(Role.name == name)
            .first()
        )

    @staticmethod
    def create(db: Session, role: Role):

        db.add(role)
        db.commit()
        db.refresh(role)

        return role