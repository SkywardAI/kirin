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
from fastapi.security import OAuth2PasswordBearer
from src.config.manager import settings
from src.api.dependencies.repository import get_repository
from src.config.settings.const import ANONYMOUS_USER
from src.models.schemas.account import AccountInResponse, AccountInUpdate, AccountWithToken
from src.repository.crud.account import AccountCRUDRepository
from src.securities.authorizations.jwt import jwt_generator, jwt_required
from src.utilities.exceptions.database import EntityDoesNotExist
from src.utilities.exceptions.http.exc_404 import http_404_exc_id_not_found_request, http_404_exc_username_not_found_request
from src.utilities.exceptions.http.exc_401 import http_exc_401_cunauthorized_request

router = fastapi.APIRouter(prefix="/accounts", tags=["accounts"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/verify")

@router.get(
    path="",
    name="accounts:read-accounts",
    response_model=list[AccountInResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_accounts(
    token: str = fastapi.Depends(oauth2_scheme),
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    jwt_payload: dict = fastapi.Depends(jwt_required)
) -> list[AccountInResponse]:
    """
    Get a list of accounts

    This endpoint retrieves all accounts in the database.

    It requires an admin token to access.

    ```bash
    curl -X 'GET' 'http://127.0.0.1:8000/accounts'
    -H 'accept: application/json'
    -H 'Authorization: Bearer {admin_token}'
    ```

    Returns a list of AccountInResponse objects:
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
    db_accounts = await account_repo.read_accounts()
    db_account_list: list = list()
    if jwt_payload.username != settings.ADMIN_USERNAME:
        raise await http_exc_401_cunauthorized_request()

    for db_account in db_accounts:
        access_token = jwt_generator.generate_access_token(account=db_account)
        account = AccountInResponse(
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
        db_account_list.append(account)

    return db_account_list


@router.get(
    path="/{id}",
    name="accounts:read-account-by-id",
    response_model=AccountInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_account(
    id: int,
    token: str = fastapi.Depends(oauth2_scheme),
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    jwt_payload: dict = fastapi.Depends(jwt_required)
) -> AccountInResponse:
    """
    Get an account by id

    This endpoint retrieves an account by id.

    It requires an admin token or the token of the account to access.

    ```bash
    curl -X 'GET' 'http://127.0.0.1:8000/accounts/{id}'
    -H 'accept: application/json'
    -H 'Authorization: Bearer {valid_token}'
    ```

    Returns an AccountInResponse object:

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
        db_account = await account_repo.read_account_by_id(id=id)
        access_token = jwt_generator.generate_access_token(account=db_account)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)
    if jwt_payload.username != settings.ADMIN_USERNAME:
        current_user = await account_repo.read_account_by_username(username=jwt_payload.username)
        if current_user != db_account:
            raise await http_exc_401_cunauthorized_request()
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

@router.patch(
    path="",
    name="accounts:update-current-account",
    response_model=AccountInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_account(
    token: str = fastapi.Depends(oauth2_scheme),
    account_update: AccountInUpdate = fastapi.Body(...),
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    jwt_payload: dict = fastapi.Depends(jwt_required)
) -> AccountInResponse:
    """
    update current account info
    email and password are optional

    **Example**

    ```bash
    curl -X 'PATCH' \
    'http://127.0.0.1:8000/api/accounts' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFiYyIsImVtYWlsIjoiYWJjQGV4YW1wbGUuY29tIiwiZXhwIjoxNzIxMjg5Mjg5LCJzdWIiOiJZT1VSLUpXVC1TVUJKRUNUIn0.10sOf9REVbh9_7xh6ROffk1J9eEkNiJctjHEr2VMJp0' \
    -H 'Content-Type: application/json' \
    -d '{
    "email": "abc@abc.com",
    "password": "abc"
    }'
    ```
    **Note:**

    anonymous user could not be updated

    **Returns**

    {
    "id": 3,
    "authorizedAccount": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFiYyIsImVtYWlsIjoiYWJjQGFiYy5jb20iLCJleHAiOjE3MjEyODkzMjMsInN1YiI6IllPVVItSldULVNVQkpFQ1QifQ.JS1COs7ViBriPcy5lqlb7rxfOuX2tOvFP5aR6iU3Fa4",
        "username": "abc",
        "email": "abc@abc.com",
        "isVerified": false,
        "isActive": false,
        "isLoggedIn": true,
        "createdAt": "2024-07-12T13:53:47.429404Z",
        "updatedAt": "2024-07-12T13:55:22.784769Z"
    }
    }

    """
    if jwt_payload.username == ANONYMOUS_USER:
        raise await http_exc_401_cunauthorized_request()
    current_user = await account_repo.read_account_by_username(username=jwt_payload.username)

    try:
        updated_db_account = await account_repo.update_account_by_id(id=current_user.id, account_update=account_update)

    except EntityDoesNotExist:
        raise await http_404_exc_username_not_found_request(username=jwt_payload.username)
    access_token = jwt_generator.generate_access_token(account=updated_db_account)

    return AccountInResponse(
        id=updated_db_account.id,
        authorized_account=AccountWithToken(
            token=access_token,
            username=updated_db_account.username,
            email=updated_db_account.email,  # type: ignore
            is_verified=updated_db_account.is_verified,
            is_active=updated_db_account.is_active,
            is_logged_in=updated_db_account.is_logged_in,
            created_at=updated_db_account.created_at,
            updated_at=updated_db_account.updated_at,
        ),
    )

@router.patch(
    path="/{id}",
    name="accounts:update-account-by-id",
    response_model=AccountInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_account_by_admin(
    query_id: int,
    token: str = fastapi.Depends(oauth2_scheme),
    account_update: AccountInUpdate = fastapi.Body(...),
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    jwt_payload: dict = fastapi.Depends(jwt_required)
) -> AccountInResponse:
    """
    update account info by account id
    this can be only done by admin
    email and password are optional

    **Example**

    ```bash
    curl -X 'PATCH' \
    'http://127.0.0.1:8000/api/accounts/{id}?query_id=3' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZW1haWwiOiJhZG1pbkBhZG1pbi5jb20iLCJleHAiOjE3MjEyODk0NTQsInN1YiI6IllPVVItSldULVNVQkpFQ1QifQ.8nz68k6fGS2seP_3ZaDCJmolR103JqH80VraEDinytM' \
    -H 'Content-Type: application/json' \
    -d '{
    "email": "user@example.com",
    "password": "string"
    }'
    ```

    **Returns**

    {
    "id": 3,
    "authorizedAccount": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFiYyIsImVtYWlsIjoidXNlckBleGFtcGxlLmNvbSIsImV4cCI6MTcyMTI4OTQ2Nywic3ViIjoiWU9VUi1KV1QtU1VCSkVDVCJ9.KqpTpviN2yTnaDZefa_vVXS6_YQJgtl2oXemd2qDTAo",
        "username": "abc",
        "email": "user@example.com",
        "isVerified": false,
        "isActive": false,
        "isLoggedIn": true,
        "createdAt": "2024-07-12T13:57:10.019039Z",
        "updatedAt": "2024-07-12T13:57:47.261777Z"
    }
    }

    """
    if jwt_payload.username != settings.ADMIN_USERNAME:
        raise await http_exc_401_cunauthorized_request()
    try:
        updated_db_account = await account_repo.update_account_by_id(id=query_id, account_update=account_update)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=query_id)
    access_token = jwt_generator.generate_access_token(account=updated_db_account)

    return AccountInResponse(
        id=updated_db_account.id,
        authorized_account=AccountWithToken(
            token=access_token,
            username=updated_db_account.username,
            email=updated_db_account.email,  # type: ignore
            is_verified=updated_db_account.is_verified,
            is_active=updated_db_account.is_active,
            is_logged_in=updated_db_account.is_logged_in,
            created_at=updated_db_account.created_at,
            updated_at=updated_db_account.updated_at,
        ),
    )


@router.delete(path="", name="accounts:delete-account-by-id", status_code=fastapi.status.HTTP_200_OK)
async def delete_account(
    id: int, account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    token: str = fastapi.Depends(oauth2_scheme),
    jwt_payload: dict = fastapi.Depends(jwt_required)
) -> dict[str, str]:
    """
    Delete an account by id

    This endpoint deletes an existing account by its ID.

    It is **IRREVERSIBLE** and should be used with caution.

    It requires an admin token to access.

    ```bash
    curl -X 'DELETE' 'http://127.0.0.1:8000/accounts/{id}'
    -H 'accept: application/json'
    -H 'Authorization: Bearer {admin_token}'
    ```

    Returns a dictionary:

    - **notification**: The deletion result
    """
    if jwt_payload.username != settings.ADMIN_USERNAME:
        raise await http_exc_401_cunauthorized_request()
    try:
        deletion_result = await account_repo.delete_account_by_id(id=id)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return {"notification": deletion_result}
