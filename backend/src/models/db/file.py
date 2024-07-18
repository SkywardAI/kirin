import sqlalchemy
from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column

from src.repository.table import Base


class UploadedFile(Base):  # type: ignore
    __tablename__ = "uploaded_file"

    id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(primary_key=True, autoincrement="auto")
    name: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(sqlalchemy.String(length=64), nullable=False, unique=True)

    __mapper_args__ = {"eager_defaults": True}
