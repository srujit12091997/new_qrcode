import logging.config
import os
import base64
from typing import Dict, List
from dotenv import load_dotenv
from jose import jwt
from datetime import datetime, timedelta, timezone
import validators
from urllib.parse import urlparse, urlunparse
from app.config import ADMIN_PASSWORD, ADMIN_USER, ALGORITHM, SECRET_KEY

# Load environment configurations for secure and configurable operations.
load_dotenv()

def initialize_logging():
    log_config_rel_path = os.path.join(os.path.dirname(__file__), '..', '..', 'logging.conf')
    log_config_abs_path = os.path.abspath(log_config_rel_path)
    logging.config.fileConfig(log_config_abs_path, disable_existing_loggers=False)

def verify_credentials(user_id: str, user_pass: str):
    if user_id == ADMIN_USER and user_pass == ADMIN_PASSWORD:
        return {"username": user_id}
    logging.warning(f"User verification failed: {user_id}")
    return None

def issue_token(data: dict, expires_delta: timedelta = None):
    token_data = data.copy()
    expiration_time = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    token_data["exp"] = expiration_time
    return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

def confirm_and_clean_url(provided_url: str):
    # Ensure the URL is a string when parsed
    parsed_url = urlparse(str(provided_url))
    if parsed_url.scheme and parsed_url.netloc:
        return urlunparse(parsed_url)
    logging.error(f"URL check failed for: {provided_url}")
    return None

def url_to_safe_string(valid_url):
    # Ensure the URL is converted to string if it's a special Pydantic URL type
    if clean_url := confirm_and_clean_url(str(valid_url)):
        return base64.urlsafe_b64encode(clean_url.encode('utf-8')).decode('utf-8').rstrip('=')
    raise ValueError("URL is invalid and cannot be transformed.")


def base64_to_url(safe_string: str) -> str:
    padding = '=' * (4 - len(safe_string) % 4)
    safe_string += padding
    original_url_bytes = base64.urlsafe_b64decode(safe_string)
    return original_url_bytes.decode('utf-8')

def craft_resource_links(verb: str, qr_file: str, api_base: str, qr_download_link: str):
    links = []
    if verb == "create":
        links.append({
            "relation": "view",
            "target": qr_download_link,
            "method": "GET",
            "content_type": "image/png"
        })
    if verb in ["create", "delete"]:
        qr_delete_endpoint = f"{api_base}/qr-codes/{qr_file}"
        links.append({
            "relation": "delete",
            "target": qr_delete_endpoint,
            "method": "DELETE",
            "content_type": "application/json"
        })
    return links
