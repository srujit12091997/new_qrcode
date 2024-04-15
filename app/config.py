

# Standard library imports and dotenv for environment management
import os
from pathlib import Path
from dotenv import load_dotenv

# Initialize environment variables from a .env file using the dotenv package.
# This practice helps to keep configuration separate from the codebase.
load_dotenv()

# Configuration Variables

# The storage location for QR code images, falling back to a default if not set.
QR_STORAGE_PATH = Path(os.getenv('QR_STORAGE_DIRECTORY', 'qr_codes_storage'))

# QR code's primary color setting, defaulting to 'crimson' if not set.
QR_CODE_COLOR = os.getenv('QR_CODE_COLOR', 'crimson')

# Background color for QR code, with a fallback default color of 'offwhite'.
QR_BACKGROUND_HUE = os.getenv('QR_BACKGROUND_HUE', 'offwhite')

# The root URL for the service, utilized for crafting response URLs.
# It defaults to the local server address on port 80.
SERVICE_ROOT_URL = os.getenv('SERVICE_ROOT_URL', 'http://127.0.0.1:80')

# Directory for stored files accessible for client download, such as QR code images.
FILE_SERVE_DIRECTORY = os.getenv('FILE_SERVE_DIRECTORY', 'file_downloads')

# The secret key for secure operations, like JWT token signing, should remain confidential.
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret")

# Preferred method for encoding and decoding JWT tokens.
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Lifespan of an access token, expressed in minutes, with a default of 30 minutes.
TOKEN_LIFETIME_MINUTES = int(os.getenv("TOKEN_LIFETIME_MINUTES", 30))

# Sample administrator credentials for the demonstration.
# In a live system, replace with a secure authentication system.
ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'secret')
