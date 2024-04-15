import os
from typing import List
import qrcode
import logging
from pathlib import Path
from app.config import SERVICE_ROOT_URL, FILE_SERVE_DIRECTORY

def retrieve_qr_file_names(qr_folder: Path) -> List[str]:
    """
    Obtain a list of all QR code file names within a given directory.
    
    Arguments:
    - qr_folder (Path): Path to the directory that holds QR code files.
    
    Returns:
    - A list containing the file names of all QR codes within the directory.
    """
    try:
        # Fetch all '.png' files located in the given directory.
        return [filename for filename in os.listdir(qr_folder) if filename.endswith('.png')]
    except FileNotFoundError:
        logging.error(f"Could not find the directory: {qr_folder}")
        raise
    except OSError as error:
        logging.error(f"OS error encountered during QR retrieval: {error}")
        raise

def create_qr_image(content: str, destination: Path, qr_color: str = 'red', background: str = 'white', module_size: int = 10):
    """
    Craft a QR code image from the supplied content and store it at the specified location.
    
    Arguments:
    - content (str): Data to be encoded in the QR code.
    - destination (Path): File path where the QR code image will be saved.
    - qr_color (str): Color for the QR code content.
    - background (str): Background color for the QR code.
    - module_size (int): Dimension of each square in the QR code grid.
    """
    logging.debug("Initiating QR code creation")
    try:
        qr_instance = qrcode.QRCode(version=1, box_size=module_size, border=5)
        qr_instance.add_data(content)
        qr_instance.make(fit=True)
        qr_img = qr_instance.make_image(fill_color=qr_color, back_color=background)
        qr_img.save(str(destination))
        logging.info(f"Stored QR code at {destination}")
    except Exception as error:
        logging.error(f"QR code creation/storage failed: {error}")
        raise

def remove_qr_image(qr_file: Path):
    """
    Erase a QR code image file from the given path.
    
    Arguments:
    - qr_file (Path): Path to the QR code image file to be removed.
    """
    if qr_file.is_file():
        qr_file.unlink()  # Perform the file deletion
        logging.info(f"Deleted QR code file {qr_file.name} successfully")
    else:
        logging.error(f"QR code file {qr_file.name} could not be located for removal")
        raise FileNotFoundError(f"QR code file {qr_file.name} could not be located")

def establish_directory_if_missing(dir_path: Path):
    """
    Construct a directory at the provided path if it is not already present.
    
    Arguments:
    - dir_path (Path): Path where the directory is to be established.
    """
    logging.debug('Attempting directory creation')
    try:
        dir_path.mkdir(parents=True, exist_ok=True)  # Make the directory, along with any parents if necessary
    except FileExistsError:
        logging.info(f"The directory already exists: {dir_path}")
    except PermissionError as error:
        logging.error(f"Denied permission to create directory at {dir_path}: {error}")
        raise
    except Exception as error:
        logging.error(f"An unexpected error occurred while creating directory at {dir_path}: {error}")
        raise
