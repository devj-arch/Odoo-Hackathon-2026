from sqlalchemy import text

from app.core.database import engine


def main():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar()
        print("Connection OK, SELECT 1 ->", result)


if __name__ == "__main__":
    main()
