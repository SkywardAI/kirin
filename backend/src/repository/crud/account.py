

import lancedb
import loguru
from src.config.settings.const import META_LANCEDB
from datetime import datetime
from src.models.schemas.account import AccountInCreate, AccountInLogin, AccountInUpdate, Account
from src.repository.crud.base import BaseCRUDRepository
from src.securities.hashing.password import pwd_generator
from src.utilities.exceptions.database import EntityDoesNotExist
from src.utilities.exceptions.password import PasswordDoesNotMatch


class AccountCRUDRepository(BaseCRUDRepository):
    def __init__(self):
        self.db = lancedb.connect(META_LANCEDB)
        self.tbl = self.db.open_table("account")

    def create_account(self, account_create: AccountInCreate) -> Account:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hash_salt = pwd_generator.generate_salt
        new_id = self._get_next_id()
        self.tbl.add([{
        "id": new_id,
        "username": account_create.username,
        "email": account_create.email,
        "_hashed_password": pwd_generator.generate_hashed_password(
            hash_salt=hash_salt, new_password=account_create.password
        ),
        "_hash_salt": hash_salt,
        "is_verified": True,
        "is_active": True,
        "is_logged_in": True,
        "created_at": current_time,
        "updated_at": current_time
        }])
        new_account = self.tbl.search().where(f"username = '{account_create.username}'", prefilter=True).limit(1).to_list()[0]
        loguru.logger.info(f"User {account_create.username} created ")
        return Account.from_dict(new_account)

    def read_accounts(self) -> list[Account]:
        loguru.logger.info("Read all accounts")
        accounts_dict_list = self.tbl.search().to_list()
        return [Account.from_dict(account_dict) for account_dict in accounts_dict_list]

    def read_account_by_id(self, id: int) -> Account:
        try:
            account = self.tbl.search().where(f"id = {id}", prefilter=True).limit(1).to_list()[0]
        except Exception as e:
            loguru.logger.error(f"{e}")
            raise EntityDoesNotExist("Account with id `{id}` does not exist!")
        loguru.logger.info(f"Read user {id}")
        return Account.from_dict(account)

    def read_account_by_username(self, username: str) -> Account:
        try:
            account = self.tbl.search().where(f"username = '{username}'", prefilter=True).limit(1).to_list()[0]
        except Exception as e:
            loguru.logger.error(f"{e}")
            raise EntityDoesNotExist("Account with username `{username}` does not exist!")
        loguru.logger.info(f"Read user {username}")
        return Account.from_dict(account)

    def read_account_by_email(self, email: str) -> Account:
        try:
            account = self.tbl.search().where(f"username = '{email}'", prefilter=True).limit(1).to_list()[0]
        except Exception as e:
            loguru.logger.error(f"{e}")
            raise EntityDoesNotExist("Account with email `{email}` does not exist!")
        loguru.logger.info(f"Read user {email}")
        return Account.from_dict(account)

    def read_user_by_password_authentication(self, account_login: AccountInLogin) -> Account:
        try:
            account = self.tbl.search().where(f"username = '{account_login.username}'", prefilter=True).limit(1).to_list()[0]
        except Exception as e:
            loguru.logger.error(f"{e}")
            raise EntityDoesNotExist("Account with username `{account_login.username}` does not exist!")
        try:
            hash_salt=account.get("_hash_salt")
            if not pwd_generator.is_password_authenticated(
                hash_salt=hash_salt, password=account_login.password, hashed_password=account.get("_hashed_password")
            ):  # type: ignore
                raise PasswordDoesNotMatch("Password does not match!")
        except Exception as e:
            loguru.logger.error(f"{e}")
        loguru.logger.info(f"Read user {account_login.username} with password authentication")
        return Account.from_dict(account)  # type: ignore

    def update_account_by_id(self, id: int, account_update: AccountInUpdate) -> Account:
        try:
            self.tbl.search().where(f"id = {id}", prefilter=True).limit(1).to_list()[0]
        except Exception as e:
            loguru.logger.error(f"{e}")
            raise EntityDoesNotExist("Account with id `{id}` does not exist!")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if account_update.email:
            self.tbl.update(where=f"id = {id}", values={"email": account_update.email, "updated_at": current_time})
        if account_update.password:
            self.tbl.update(where=f"id = {id}", values={
                "_hashed_password": pwd_generator.generate_hashed_password(
                            hash_salt=pwd_generator.generate_salt, new_password=account_update.password
                            ),
                "_hash_salt": pwd_generator.generate_salt,
                "updated_at": current_time})
        update_account = self.tbl.search().where(f"id = {id}", prefilter=True).limit(1).to_list()[0]
        loguru.logger.info(f"Update user {id}")
        return Account.from_dict(update_account)

    def delete_account_by_id(self, id: int) -> str:
        try:
            self.tbl.delete(f"id = {id}")
        except Exception as e:
            loguru.logger.error(f"{e}")
            raise EntityDoesNotExist(f"Account with id `{id}` does not exist!")  # type: ignore
        loguru.logger.info(f"Delete user {id}")
        return f"Account with id '{id}' is successfully deleted!"

    def is_username_taken(self, username: str) -> bool:
        try:
            self.tbl.search().where(f"username = '{username}'", prefilter=True).limit(1).to_list()[0]
        except Exception :
            return True
        return False

    def is_email_taken(self, email: str) -> bool:
        try:
            self.tbl.search().where(f"email = '{email}'", prefilter=True).limit(1).to_list()[0]
        except Exception :
            return True
        return False

    def _get_next_id(self):
        tbl = self.db.open_table("next_id")
        next_id = tbl.search().select(["id"]).limit(1).to_list()[0].get("id")
        tbl.update(where=f"id = {next_id}", values={"id":next_id+1})
        return next_id
