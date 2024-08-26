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
import lancedb
import loguru
import uuid
import time
from datetime import datetime
from src.config.settings.const import META_LANCEDB
from src.models.schemas.chat import SessionUpdate, Chats, Session, ChatHistory
from src.repository.crud.base import BaseCRUDRepository
from src.utilities.exceptions.database import EntityDoesNotExist

class SessionCRUDRepository(BaseCRUDRepository):
    def __init__(self):
        self.db = lancedb.connect(META_LANCEDB)
        self.tbl = self.db.open_table("session")
        
    def create_session(self, account_id: int, name: str) -> Session:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        uuid_id=str(uuid.uuid4())
        self.tbl.add([{
            "session_uuid": uuid_id,
            "account_id": account_id,
            "name": name,
            "session_type": "chat",
            "dataset_name": "",
            "created_at": current_time
        }])
        new_session = self.tbl.search().where(f"session_uuid = '{uuid_id}'", prefilter=True).limit(1).to_list()[0]
        loguru.logger.info(f"Session {name} {uuid_id} created ")
        return Session.from_dict(new_session) 

    def read_sessions(self) -> list[Session]:
        loguru.logger.info("Read all sesssion")
        session_dict_list = self.tbl.search().to_list()
        return [Session.from_dict(session_dict) for session_dict in session_dict_list]

    def read_sessions_by_uuid(self, session_uuid: str) -> Session:
        try:
            session = self.tbl.search().where(f"session_uuid = '{session_uuid}'", prefilter=True).limit(1).to_list()[0]
        except Exception as e:
            loguru.logger.error(f"{e}")
            raise EntityDoesNotExist("Session with uuid `{session_uuid}` does not exist!")
        loguru.logger.info(f"Read session with {session_uuid}")
        return Session.from_dict(session)

    def update_sessions_by_uuid(self, session: SessionUpdate, account_id: int) -> Session:
        try:
            self.tbl.search().where(f"session_uuid = '{session.sessionUuid}' , account_id = {account_id}", prefilter=True).limit(1).to_list()[0]
        except Exception as e:
            loguru.logger.error(f"{e}")
            raise EntityDoesNotExist("Session with uuid `{session.session_uuid}}` does not exist!")
        
        if session.name:
            self.tbl.update(where=f"session_uuid = '{session.sessionUuid}'", values={"name": session.name})
        if session.session_type:
            self.tbl.update(where=f"session_uuid = '{session.sessionUuid}'", values={"session_type": session.session_type})
        update_session = self.tbl.search().where(f"session_uuid = '{session.sessionUuid}'", prefilter=True).limit(1).to_list()[0]
        loguru.logger.info(f"Update session {session.sessionUuid}")
        return Session.from_dict(update_session)

    def delete_session_by_uuid(self, uuid: str, account_id: int) -> Session:
        if account_id == 0:
            try:
                self.tbl.search().where(f"session_uuid = '{uuid}'", prefilter=True).limit(1).to_list()[0]
            except Exception as e:
                loguru.logger.error(f"{e}")
                raise EntityDoesNotExist("Session with uuid `{session.session_uuid}}` does not exist!")
        else:
            try:
                self.tbl.search().where(f"session_uuid = '{uuid}' , account_id = {account_id}", prefilter=True).limit(1).to_list()[0]
            except Exception as e:
                loguru.logger.error(f"{e}")
                raise EntityDoesNotExist("Session with uuid `{session.session_uuid}}` does not exist!")
        try:
            self.tbl.delete(f"session_uuid = '{uuid}'")
        except Exception as e:
            loguru.logger.error(f"{e}")
            raise EntityDoesNotExist(f"Session with uuid `{uuid}` does not exist!")  # type: ignore
        loguru.logger.info(f"Delete session {uuid}")
        return f"Session with uuid '{uuid}' is successfully deleted!"

    def append_ds_name_to_session(self, session_uuid: str, account_id: int, ds_name: str) -> Session:
        """
        Append the dataset name to specific session of the specific account

        Args:
            session_uuid (str): Session UUID
            account_id (int): Account ID
            ds_name (str): Dataset Name

        Returns:
            Session: Updated Session instance
        """
        try:
            self.tbl.search().where(f"session_uuid = '{session_uuid}' , account_id = {account_id}", prefilter=True).limit(1).to_list()[0]
        except Exception as e:
            loguru.logger.error(f"{e}")
            raise EntityDoesNotExist("Session with uuid `{session_uuid}}` does not exist!")

        self.tbl.update(where=f"session_uuid = '{session_uuid}'", values={"dataset_name": ds_name})
        loguru.logger.info(f"Update session {session_uuid}")
        update_session = self.tbl.search().where(f"session_uuid = '{session_uuid}'", prefilter=True).limit(1).to_list()[0]
        loguru.logger.info(f"Update session {session_uuid}")
        return Session.from_dict(update_session)

    def read_create_sessions_by_uuid(self, session_uuid: str, account_id: int, name: str, session_type: str = "chat") -> Session:
        try:
            session=self.tbl.search().where(f"session_uuid = '{session_uuid}' , account_id = {account_id}", prefilter=True).limit(1).to_list()[0]
        except Exception:
            loguru.logger.info(f"Session with uuid `{session_uuid}` does not exist! Create new one")
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            uuid_id=str(uuid.uuid4())
            self.tbl.add([{
                "session_uuid": uuid_id,
                "account_id": account_id,
                "name": name,
                "session_type": session_type,
                "dataset_name": "",
                "created_at": current_time
            }])
            session = self.tbl.search().where(f"session_uuid = '{uuid_id}'", prefilter=True).limit(1).to_list()[0]
        return Session.from_dict(session)

    def read_sessions_by_account_id(self, id: int) -> list[Session]:
        loguru.logger.info(f"Read all sesssion of account id {id}")
        try:
            session_dict_list = self.tbl.search().where(f"account_id = {id}", prefilter=True).to_list()
        except Exception as e:
            loguru.logger.error(f"{e}")
            raise EntityDoesNotExist("Session with account `{id}}` does not exist!")
        return [Session.from_dict(session_dict) for session_dict in session_dict_list]

    def verify_session_by_account_id(self, session_uuid: str, account_id: int) -> bool:
        try:
            self.tbl.search().where(f"session_uuid = '{session_uuid}' , account_id = {account_id}", prefilter=True).limit(1).to_list()[0]
            return True
        except Exception as e:
            loguru.logger.error(f"{e}")
            return False


class ChatHistoryCRUDRepository(BaseCRUDRepository):
    def __init__(self):
        self.db = lancedb.connect(META_LANCEDB)
        self.tbl = self.db.open_table("chat_history")

    def read_chat_history_by_session_uuid(self, uuid: str, limit_num=50) -> list[ChatHistory]:
        loguru.logger.info(f"Read all chat history of session uuid {uuid}")
        try:
            chat_history_list = self.tbl.search().where(f"session_uuid = '{uuid}'", prefilter=True).limit(limit_num).to_list()
        except Exception as e:
            loguru.logger.error(f"{e}")
            raise EntityDoesNotExist("Chat history with session uuid `{uuid}}` does not exist!")
        return [ChatHistory.from_dict(chat_history) for chat_history in chat_history_list]

    def load_create_chat_history(self, session_uuid: str, chats: list[Chats]):
        try:
            for chat in chats:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                self.tbl.add([{
                    "session_uuid": session_uuid,
                    "role": chat.role,
                    "message": chat.message[:4096],
                    "created_at": current_time
                }])
                time.sleep(0.001)
        except Exception as e:
            loguru.logger.error(f"Error: {e}")
