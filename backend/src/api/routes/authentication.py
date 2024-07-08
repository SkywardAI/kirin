import fastapi
from typing import Annotated
from src.api.dependencies.repository import get_repository
from src.models.schemas.account import AccountInCreate, AccountInLogin, AccountInResponse, AccountWithToken
from src.config.settings.const import ANONYMOUS_USER,ANONYMOUS_PASS
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
        await account_repo.is_username_taken(username=account_create.username)
        await account_repo.is_email_taken(email=account_create.email)

    except EntityAlreadyExists:
        raise await http_exc_400_credentials_bad_signup_request()

    new_account = await account_repo.create_account(account_create=account_create)
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

    if account_login.username == ANONYMOUS_USER:
        raise await http_exc_400_credentials_bad_signin_request()
    
    try:
        db_account = await account_repo.read_user_by_password_authentication(account_login=account_login)

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
async def get_chathistory(
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository))
) -> dict:
    anonymous_user = AccountInLogin(username=ANONYMOUS_USER, password=ANONYMOUS_PASS)
    db_account = await account_repo.read_user_by_password_authentication(account_login=anonymous_user)
    access_token = jwt_generator.generate_access_token(account=db_account)

    return {"token": access_token}

@router.post("/verify")
async def login_for_access_token(
    form_data: Annotated[fastapi.security.OAuth2PasswordRequestForm, fastapi.Depends()],
    account_repo: AccountCRUDRepository = fastapi.Depends(get_repository(repo_type=AccountCRUDRepository)),
):
    """
    verify the user and return the access token
    """
    try:
        db_account= await account_repo.read_user_by_password_authentication(
            account_login=AccountInLogin(username=form_data.username,password=form_data.password))
    except Exception:
        raise await http_exc_400_failed_validate_request()
    access_token = jwt_generator.generate_access_token(account=db_account)
    return {"access_token": access_token, "token_type": "bearer"}
