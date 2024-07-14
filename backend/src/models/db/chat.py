import datetime
import sqlalchemy
import uuid

from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.repository.table import Base


class Session(Base):  # type: ignore
    __tablename__ = "session"

    id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(primary_key=True, autoincrement="auto")
    uuid: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(sqlalchemy.String(length=36), nullable=False, default=lambda: str(uuid.uuid4()))
    account_id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(nullable=True)
    name: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(sqlalchemy.String(length=64), nullable=True)
    type: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(sqlalchemy.Enum("rag", "chat", name="session_type"), nullable=False, default="chat")
    created_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=False, server_default=sqlalchemy_functions.now()
    )
    updated_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        server_onupdate=sqlalchemy.schema.FetchedValue(for_update=True),
    )
    __mapper_args__ = {"eager_defaults": True}


class ChatHistory(Base):  # type: ignore
    __tablename__ = "chat_history"

    id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(primary_key=True, autoincrement="auto")
    session_id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(nullable=False)
    role: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(sqlalchemy.Enum("user", "assistant", name="role"), nullable=False, default="user")
    message: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(sqlalchemy.String(length=4096), nullable=False)
    created_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=False, server_default=sqlalchemy_functions.now()
    )

    __mapper_args__ = {"eager_defaults": True}
