from typing import Optional

from pydantic import BaseModel, Field


class noteSchema(BaseModel):
    title: str = Field(...)
    note: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "title": "note title",
                "note": "note details here",
            }
        }


class UpdatenoteModel(BaseModel):
    title: Optional[str]
    note: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "note title",
                "note": "note details here",
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
