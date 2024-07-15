import fastapi
from fastapi.security import OAuth2PasswordBearer
import pydantic
from src.config.manager import settings
from src.api.dependencies.repository import get_repository
from src.models.schemas.account import AccountInResponse, AccountInUpdate, AccountWithToken
from src.repository.crud.account import AccountCRUDRepository
from src.securities.authorizations.jwt import jwt_generator, jwt_required
from src.utilities.exceptions.database import EntityDoesNotExist
from src.utilities.exceptions.http.exc_404 import http_404_exc_id_not_found_request
from src.utilities.exceptions.http.exc_401 import http_exc_401_cunauthorized_request

router = fastapi.APIRouter(prefix="/accounts", tags=["accounts"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/verify")

@router.get(
    path="",
    name="accountss:read-accounts",
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
    name="accountss:read-account-by-id",
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
    path="/{id}",
    name="accountss:update-account-by-id",
    response_model=AccountInResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def update_account(
    query_id: int,
    token: str = fastapi.Depends(oauth2_scheme),
    update_username: str | None = None,
    update_email: pydantic.EmailStr | None = None,
    update_password: str | None = None,
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    jwt_payload: dict = fastapi.Depends(jwt_required)
) -> AccountInResponse:
    account_update = AccountInUpdate(username=update_username, email=update_email, password=update_password)
    try:
        updated_db_account = await account_repo.update_account_by_id(id=query_id, account_update=account_update)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=query_id)
    if jwt_payload.username != settings.ADMIN_USERNAME:
        current_user = await account_repo.read_account_by_username(username=jwt_payload.username)
        if current_user != updated_db_account:
            raise await http_exc_401_cunauthorized_request()

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


@router.delete(path="", name="accountss:delete-account-by-id", status_code=fastapi.status.HTTP_200_OK)
async def delete_account(
    id: int, account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
    token: str = fastapi.Depends(oauth2_scheme),
    jwt_payload: dict = fastapi.Depends(jwt_required)
) -> dict[str, str]:
    if jwt_payload.username != settings.ADMIN_USERNAME:
        raise await http_exc_401_cunauthorized_request()
    try:
        deletion_result = await account_repo.delete_account_by_id(id=id)

    except EntityDoesNotExist:
        raise await http_404_exc_id_not_found_request(id=id)

    return {"notification": deletion_result}
