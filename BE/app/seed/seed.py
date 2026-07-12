from app.core.database import SessionLocal
from app.models.role import Role
from app.models.user import User
from app.core.security import hash_password


db = SessionLocal()


roles = [
    "Admin",
    "Fleet Manager",
    "Dispatcher",
    "Safety Officer",
    "Financial Analyst"
]


for role_name in roles:

    role = db.query(Role).filter(Role.name == role_name).first()

    if not role:

        db.add(
            Role(
                name=role_name
            )
        )

db.commit()


admin_role = db.query(Role).filter(Role.name == "Admin").first()


admin = db.query(User).filter(
    User.email == "admin@transitops.com"
).first()


if not admin:

    admin = User(
        name="System Admin",
        email="admin@transitops.com",
        password_hash=hash_password("admin123"),
        role_id=admin_role.id,
    )

    db.add(admin)

    db.commit()

print("Database Seeded Successfully")