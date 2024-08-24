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

import fastapi
import loguru
from typing import Annotated
from src.api.dependencies.repository import get_repository
from src.models.schemas.account import AccountInCreate, AccountInLogin, AccountInResponse, AccountWithToken
from src.config.settings.const import ANONYMOUS_USER, ANONYMOUS_PASS
from src.repository.crud.account import AccountCRUDRepository
from src.securities.authorizations.jwt import jwt_generator
from src.utilities.exceptions.database import EntityAlreadyExists
from src.utilities.exceptions.http.exc_400 import (
    http_exc_400_credentials_bad_signin_request,
    http_exc_400_credentials_bad_signup_request,
    http_exc_400_failed_validate_request,
)

router = fastapi.APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/signup",
    name="auth:signup",
    response_model=AccountInResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def signup(
    account_create: AccountInCreate,
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
) -> AccountInResponse:
    """
    Create a new account

    ```bash
    curl -X 'POST' 'http://127.0.0.1:8000/api/auth/signup'
    -H 'accept: application/json'
    -H 'Content-Type: application/json'
    -d '{"username": "aisuko", "email": "aisuko@example.com", "password": "aisuko"}'
    ```

    Returns AccountInResponse:
    - **id**: The id of the account
    - **authorized_account**: The account with token
        - **token**: The access token
        - **username**: The username
        - **email**: The email
        - **is_verified**: The verification status
        - **is_active**: The activation status
        - **is_logged_in**: The login status
        - **created_at**: The creation time
        - **updated_at**: The update time
    """

    try:
        account_repo.is_username_taken(username=account_create.username)
        account_repo.is_email_taken(email=account_create.email)

    except EntityAlreadyExists:
        raise await http_exc_400_credentials_bad_signup_request()

    new_account = account_repo.create_account(account_create=account_create)
    access_token = jwt_generator.generate_access_token(account=new_account)

    return AccountInResponse(
        id=new_account.id,
        authorized_account=AccountWithToken(
            token=access_token,
            username=new_account.username,
            email=new_account.email,  # type: ignore
            is_verified=new_account.is_verified,
            is_active=new_account.is_active,
            is_logged_in=new_account.is_logged_in,
            created_at=new_account.created_at,
            updated_at=new_account.updated_at,
        ),
    )


@router.post(
    path="/signin",
    name="auth:signin",
    response_model=AccountInResponse,
    status_code=fastapi.status.HTTP_202_ACCEPTED,
)
async def signin(
    account_login: AccountInLogin,
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
) -> AccountInResponse:
    """
    Sign in an existing account

    ```bash
    curl -X 'POST' 'http://127.0.0.1:8000/api/auth/signin'
    -H 'accept: application/json'
    -H 'Content-Type: application/json'
    -d '{"username": "enota", "password": "enota"}'
    ```

    Returns AccountInResponse:
    - **id**: The id of the account
    - **authorized_account**: The account with token
        - **token**: The access token
        - **username**: The username
        - **email**: The email
        - **is_verified**: The verification status
        - **is_active**: The activation status
        - **is_logged_in**: The login status
        - **created_at**: The creation time
        - **updated_at**: The update time
    """

    if account_login.username == ANONYMOUS_USER:
        raise await http_exc_400_credentials_bad_signin_request()

    try:
        db_account = account_repo.read_user_by_password_authentication(account_login=account_login)

    except Exception:
        raise await http_exc_400_credentials_bad_signin_request()

    access_token = jwt_generator.generate_access_token(account=db_account)

    return AccountInResponse(
        id=db_account.id,
        authorized_account=AccountWithToken(
            token=access_token,
            username=db_account.username,
            email=db_account.email,  # type: ignore
            is_verified=db_account.is_verified,
            is_active=db_account.is_active,
            is_logged_in=db_account.is_logged_in,
            created_at=db_account.created_at,
            updated_at=db_account.updated_at,
        ),
    )


@router.get(
    path="/token",
    name="authentication: token for anonymous user",
    response_model=dict,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_token(
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
) -> dict:
    """
    Get chat history for an anonymous user

    ```bash
    curl -X 'GET' http://127.0.0.1:8000/api/auth/token'
    -H 'accept: application/json'

    Returns a JSON object with the token for an anonymous user:
    - **token**: The access token for the anonymous user
    """
    anonymous_user = AccountInLogin(username=ANONYMOUS_USER, password=ANONYMOUS_PASS)
    db_account = account_repo.read_user_by_password_authentication(account_login=anonymous_user)
    access_token = jwt_generator.generate_access_token(account=db_account)

    return {"token": access_token}


@router.post("/verify")
async def login_for_access_token(
    form_data: Annotated[fastapi.security.OAuth2PasswordRequestForm, fastapi.Depends()],
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
):
    """
    Verify the user and return the access token

    ```bash
    curl -X 'POST' 'http://127.0.0.1:8000/api/auth/verify'
    -H 'Content-Type: application/x-www-form-urlencoded'
    -H 'accept': application/json
    -d 'username=enota&password=enota'
    ```

    Returns a JSON object with the access token and token type:
    - **access_token**: The access token
    - **token_type**: The token type
    """
    try:
        db_account = account_repo.read_user_by_password_authentication(
            account_login=AccountInLogin(username=form_data.username, password=form_data.password)
        )
    except Exception as e:
        loguru.logger.error(f"{e}")
        raise await http_exc_400_failed_validate_request()
    access_token = jwt_generator.generate_access_token(account=db_account)
    return {"access_token": access_token, "token_type": "bearer"}
