from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_note,
    delete_note,
    retrieve_note,
    retrieve_notes,
    update_note,
)
from server.models.note import (
    ErrorResponseModel,
    ResponseModel,
    noteSchema,
    UpdatenoteModel,
)

router = APIRouter()


@router.post("/", response_description="note data added into the database")
async def add_note_data(note: noteSchema = Body(...)):
    note = jsonable_encoder(note)
    new_note = await add_note(note)
    return ResponseModel(new_note, "note added successfully.")


@router.get("/", response_description="notes retrieved")
async def get_notes():
    notes = await retrieve_notes()
    if notes:
        return ResponseModel(notes, "notes data retrieved successfully")
    return ResponseModel(notes, "Empty list returned")


@router.get("/{id}", response_description="note data retrieved")
async def get_note_data(id):
    note = await retrieve_note(id)
    if note:
        return ResponseModel(note, "note data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "note doesn't exist.")


@router.put("/{id}")
async def update_note_data(id: str, req: UpdatenoteModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_note = await update_note(id, req)
    if updated_note:
        return ResponseModel(
            "note with ID: {} name update is successful".format(id),
            "note name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the note data.",
    )


@router.delete("/{id}", response_description="note data deleted from the database")
async def delete_note_data(id: str):
    deleted_note = await delete_note(id)
    if deleted_note:
        return ResponseModel(
            "note with ID: {} removed".format(id), "note deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "note with id {0} doesn't exist".format(id)
    )
