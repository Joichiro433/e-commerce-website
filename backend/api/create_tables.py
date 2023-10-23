from sqlmodel import SQLModel

from dependencies import engine


if __name__ == '__main__':
    SQLModel.metadata.create_all(engine)
