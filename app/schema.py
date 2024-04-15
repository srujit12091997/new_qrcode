from pydantic import BaseModel, HttpUrl, Field, PositiveInt
from typing import List, Optional

class EncodeURLRequest(BaseModel):
    target_url: HttpUrl = Field(..., description="The web address to be converted into a QR code.")
    primary_color: str = Field(default="darkred", description="The QR code's primary color.", example="black")
    background_color: str = Field(default="white", description="The color behind the QR code.", example="yellow")
    dimensions: PositiveInt = Field(default=12, description="The QR code's scale, ranging between 1 and 40.", example=20)

    class Config:
        schema_extra = {
            "example": {
                "target_url": "https://yourwebsite.com",
                "primary_color": "black",
                "background_color": "yellow",
                "dimensions": 20
            }
        }

class ResourceLink(BaseModel):
    relation: str = Field(..., description="The type of relationship this link has.")
    target: HttpUrl = Field(..., description="The destination URL this link points to.")
    method: str = Field(..., description="The HTTP verb associated with this link's action.")
    content_type: str = Field(default="application/json", description="The MIME type of the link's target content.")

    class Config:
        schema_extra = {
            "example": {
                "relation": "self",
                "target": "https://api.yourwebsite.com/qr/456",
                "method": "GET",
                "content_type": "application/json"
            }
        }

class QRCodeCreationResponse(BaseModel):
    notice: str = Field(..., description="Message regarding the QR code operation.")
    qr_link: HttpUrl = Field(..., description="Direct link to the newly created QR code.")
    navigation_links: List[ResourceLink] = Field(default=[], description="HATEOAS-style navigation links for the QR code.")

    class Config:
        schema_extra = {
            "example": {
                "notice": "QR code was generated successfully.",
                "qr_link": "https://api.yourwebsite.com/qr/456",
                "navigation_links": [
                    {
                        "relation": "self",
                        "target": "https://api.yourwebsite.com/qr/456",
                        "method": "GET",
                        "content_type": "application/json"
                    }
                ]
            }
        }

class AuthToken(BaseModel):
    access_token: str = Field(..., description="Token for securing communication.")
    token_type: str = Field(default="bearer", description="Classification of the token provided.")

    class Config:
        schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

class TokenIdentity(BaseModel):
    user_identifier: Optional[str] = Field(None, description="Unique username associated with the token.")

    class Config:
        schema_extra = {
            "example": {
                "user_identifier": "uniqueuser@yourwebsite.com"
            }
        }
