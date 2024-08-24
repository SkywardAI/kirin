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


import unittest
import fastapi
from fastapi.testclient import TestClient
from src.models.schemas.account import Account
from src.repository.crud.base import BaseCRUDRepository
from src.repository.crud.account import AccountCRUDRepository
from src.api.routes import authentication


class OverAccountInCreate:
    username = "aisuko"
    email = "aisuko@rmit.edu.au"
    password: "123"


class OverAccountCRUDRepository(BaseCRUDRepository):
    def create_account(self, account_create: OverAccountInCreate):
        return Account(
            id=1,
            username=account_create.username,
            email=account_create.email,
            is_verified=True,
            is_active=True,
            is_logged_in=True,
            created_at="2024-01-01 00:00:00",
            updated_at="2024-01-01 00:00:00",
        )

    def is_username_taken(self, username: str) -> bool:
        return False

    def is_email_taken(self, email: str) -> bool:
        return False

    def generate_access_token(self, username: str) -> str:
        return "access_token"


def over_get_repository(repo_type=AccountCRUDRepository):
    return OverAccountCRUDRepository


@unittest.skip(
    "Skip the test, because the we cannot find dependencies of signup, see https://github.com/tiangolo/fastapi/discussions/8127#discussioncomment-5147586"
)
class TestAPIAuthentication(unittest.TestCase):
    """
    Test the FastAPI application attributes
    """

    @classmethod
    def setUpClass(cls):
        cls.app = fastapi.FastAPI()
        cls.app.include_router(authentication.router)
        cls.client = TestClient(cls.app)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_api_authentication(self):
        """
        Test the authentication API

        """
        self.app.dependency_overrides[AccountCRUDRepository] = over_get_repository

        response = self.client.post(
            "/auth/signup", json={"username": "aisuko", "email": "aisuko@rmit.edu.au", "password": "aisuko"}
        )
        assert response.status_code == 400
