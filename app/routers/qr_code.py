from fastapi import APIRouter, HTTPException, Depends, Response, status as response_status
from fastapi.responses import JSONResponse as JsonResponse
from fastapi.security import OAuth2PasswordBearer as OAuth2Bearer
from typing import List

from app.schema import EncodeURLRequest as QRRequest, QRCodeCreationResponse as QRResponse
from app.services.qr_service import create_qr_image, retrieve_qr_file_names, remove_qr_image
from app.utils.common import base64_to_url, url_to_safe_string, craft_resource_links
from app.config import QR_STORAGE_PATH, QR_CODE_COLOR, QR_BACKGROUND_HUE, SERVICE_ROOT_URL, FILE_SERVE_DIRECTORY

import logging

qr_router = APIRouter()
auth_scheme = OAuth2Bearer(tokenUrl="token")

@qr_router.post("/qr-codes/", response_model=QRResponse, status_code=response_status.HTTP_201_CREATED, tags=["QR Codes"])
async def generate_qr_code(payload: QRRequest, token: str = Depends(auth_scheme)):
    logging.info(f"Request received to generate QR for: {str(payload.target_url)}")  # Convert to string for logging

    # Convert to string when passing to the url_to_safe_string function
    safe_filename = url_to_safe_string(str(payload.target_url))
    if not safe_filename:
        return JsonResponse(
            status_code=response_status.HTTP_400_BAD_REQUEST,
            content={"detail": "Invalid URL provided"}
        )
    
    qr_img_name = f"{safe_filename}.png"
    full_qr_path = QR_STORAGE_PATH / qr_img_name
    download_url = f"{SERVICE_ROOT_URL}/{FILE_SERVE_DIRECTORY}/{qr_img_name}"
    resource_links = craft_resource_links("create", qr_img_name, SERVICE_ROOT_URL, download_url)
    
    if full_qr_path.exists():
        logging.info("QR already generated.")
        return JsonResponse(
            status_code=response_status.HTTP_409_CONFLICT,
            content={"detail": "Duplicate QR code.", "links": resource_links}
        )

    create_qr_image(str(payload.target_url), full_qr_path, QR_CODE_COLOR, QR_BACKGROUND_HUE, payload.dimensions)
    return QRResponse(notice="Generated QR code.", qr_link=download_url, navigation_links=resource_links)

    
    create_qr_image(payload.target_url, full_qr_path, QR_CODE_COLOR, QR_BACKGROUND_HUE, payload.dimensions)
    return QRResponse(notice="Generated QR code.", qr_link=download_url, navigation_links=resource_links)

@qr_router.get("/qr-codes/", response_model=List[QRResponse], tags=["QR Codes"])
async def show_all_qr_codes(token: str = Depends(auth_scheme)):
    logging.info("Generating list of all available QRs.")
    qr_code_files = retrieve_qr_file_names(QR_STORAGE_PATH)
    responses = [
        QRResponse(
            notice="QR code ready for use.",
            qr_link=base64_to_url(qr[:-4]),
            navigation_links=craft_resource_links("list", qr, SERVICE_ROOT_URL, f"{SERVICE_ROOT_URL}/{FILE_SERVE_DIRECTORY}/{qr}")
        ) for qr in qr_code_files
    ]
    return responses

@qr_router.delete("/qr-codes/{qr_img_name}", status_code=response_status.HTTP_204_NO_CONTENT, tags=["QR Codes"])
async def remove_qr_code(qr_img_name: str, auth_token: str = Depends(auth_scheme)):
    logging.info(f"Initiating deletion of QR code: {qr_img_name}.")
    qr_file_path = QR_STORAGE_PATH / qr_img_name
    if not qr_file_path.is_file():
        raise HTTPException(status_code=response_status.HTTP_404_NOT_FOUND, detail="Can't locate QR code")
    remove_qr_image(qr_file_path)
    return Response(status_code=response_status.HTTP_204_NO_CONTENT)
