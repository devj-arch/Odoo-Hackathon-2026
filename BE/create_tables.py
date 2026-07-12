from app.core.database import Base, engine
from app import models  # noqa: F401 - registers all tables on Base


def main():
    Base.metadata.create_all(bind=engine)
    print("Tables created:")
    for table in Base.metadata.sorted_tables:
        print(" -", table.name)


if __name__ == "__main__":
    main()
