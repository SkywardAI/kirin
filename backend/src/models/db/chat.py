# coding=utf-8

# Copyright [2024] [SkywardAI]
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import sqlalchemy
import uuid

from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column
from sqlalchemy.sql import functions as sqlalchemy_functions

from src.repository.table import Base


class Session(Base):  # type: ignore
    __tablename__ = "session"

    id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(primary_key=True, autoincrement="auto")
    uuid: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.String(length=36), nullable=False, default=lambda: str(uuid.uuid4())
    )
    account_id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(nullable=True)
    name: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(sqlalchemy.String(length=64), nullable=True)
    session_type: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.Enum("rag", "chat", name="session_type"), nullable=False, default="chat"
    )
    dataset_name: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(sqlalchemy.String(length=256), nullable=True)
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
    role: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.Enum("user", "assistant", name="role"), nullable=False, default="user"
    )
    message: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(sqlalchemy.String(length=4096), nullable=False)
    created_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True), nullable=False, server_default=sqlalchemy_functions.now()
    )

    __mapper_args__ = {"eager_defaults": True}
