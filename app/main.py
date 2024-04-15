

from fastapi import FastAPI
from app.config import QR_STORAGE_PATH as QR_PATH
from app.routers import qr_code,oauth # Adjust according to project layout
from app.services.qr_service import establish_directory_if_missing as ensure_dir_exists
from app.utils.common import initialize_logging as init_logs

# Initializes the application's logging system using predefined settings.
# Essential for tracking application behavior and troubleshooting issues.
init_logs()

# Verifies and creates, if necessary, the directory for QR code storage at application startup.
ensure_dir_exists(QR_PATH)

# Constructing the core FastAPI app object with metadata.
app = FastAPI(
    title="QR Code Operations",
    description="A service for managing QR code generation, retrieval, and deletion, with OAuth integration for protected access.",
    version="1.0.0",
        redoc_url=None,  # Disabling Redoc documentation endpoint
    contact={
        "name": "Support Team",
        "url": "http://support.yourapi.com",
        "email": "help@yourapi.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "http://www.apache.org/licenses/LICENSE-2.0.html",
    }
)

# Adding routing mechanisms to the API for various operations.
# Each router governs a distinct section of the API's functionality.
app.include_router(qr_code.qr_router)  # Incorporating QR code-related routes
app.include_router(oauth.security_router)  # Incorporating authentication routes
