import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017" 

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.notes

note_collection = database.get_collection("notes_collection")


def note_helper(note) -> dict:
    return {
        "id": str(note["_id"]),
        "title": note["title"],
        "note": note["note"],
    }


# crud operations

# Retrieve all notes present in the database
async def retrieve_notes():
    notes = []
    async for note in note_collection.find():
        notes.append(note_helper(note))
    return notes


# Add a new note into to the database
async def add_note(note_data: dict) -> dict:
    note = await note_collection.insert_one(note_data)
    new_note = await note_collection.find_one({"_id": note.inserted_id})
    return note_helper(new_note)


# Retrieve a note with a matching ID
async def retrieve_note(id: str) -> dict:
    note = await note_collection.find_one({"_id": ObjectId(id)})
    if note:
        return note_helper(note)


# Update a note with a matching ID
async def update_note(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    note = await note_collection.find_one({"_id": ObjectId(id)})
    if note:
        updated_note = await note_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_note:
            return True
        return False


# Delete a note from the database
async def delete_note(id: str):
    note = await note_collection.find_one({"_id": ObjectId(id)})
    if note:
        await note_collection.delete_one({"_id": ObjectId(id)})
        return True
