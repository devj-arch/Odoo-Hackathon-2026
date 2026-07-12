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


# name, email, password, role name
seed_users = [
    ("System Admin", "admin@transitops.com", "admin123", "Admin"),
    # Personal test account - lets you exercise the forgot-password flow
    # against a real inbox instead of the placeholder admin address.
    ("Dhir", "goplanidhir@gmail.com", "Pass1234", "Admin"),
]


for name, email, password, role_name in seed_users:

    role = db.query(Role).filter(Role.name == role_name).first()

    existing = db.query(User).filter(User.email == email).first()

    if not existing:

        user = User(
            name=name,
            email=email,
            password_hash=hash_password(password),
            role_id=role.id,
        )

        db.add(user)

        db.commit()


print("Database Seeded Successfully")