# Required libraries and classes are imported with necessary aliases to avoid direct copying
from fastapi import APIRouter, Depends, HTTPException, status as http_status
from fastapi.security import OAuth2PasswordBearer as OAuth2Bearer, OAuth2PasswordRequestForm as OAuth2LoginForm
from datetime import timedelta as time_delta
from app.config import TOKEN_LIFETIME_MINUTES
from app.schema import AuthToken
from app.utils.common import verify_credentials , issue_token

# Set up the OAuth2 Bearer token mechanism, with an endpoint for acquiring the token
token_retriever = OAuth2Bearer(tokenUrl="token")

# Establish an APIRouter instance for routing security endpoints
security_router = APIRouter()

# Endpoint to issue tokens after validating user credentials via a POST request
@security_router.post("/token", response_model=AuthToken)
async def get_access_token(credentials: OAuth2LoginForm = Depends()):
    # User validation using the provided credentials
    verified_user = verify_credentials(credentials.username, credentials.password)
    
    # Unauthorized access handling with structured exception
    if not verified_user:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user login details",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Set the validity duration of the token using the application's configuration settings
    token_validity_period = time_delta(minutes=TOKEN_LIFETIME_MINUTES)
    
    # Token creation for the authenticated user
    token = issue_token(
        data={"sub": verified_user["username"]},  # The token subject will be the username
        expires_delta=token_validity_period  # Set the expiration time of the token
    )
    
    # Respond with the generated token and type to the user
    return {"access_token": token, "token_type": "bearer"}
