from fastapi import FastAPI, UploadFile, Form
from app.mongo_db import notes_collection
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Response
from app.dependencies.authorization import get_current_user
from fastapi import HTTPException,status

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/create_notes")
async def create_note(
    title: str = Form(...),
    subject: str = Form(...),
    content: str = Form(""),
    file_url: str | None = None,
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )
    note = {
        "title": title,
        "subject": subject,
        "content": content,
        "file_url": file_url
    }

    result = notes_collection.insert_one(note)

    note["_id"] = str(result.inserted_id)
    return note



@router.get("/get_notes")
async def get_notes(
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )

    notes = []
    for note in notes_collection.find():
        note["_id"] = str(note["_id"])
        notes.append(note)

    return notes


@router.delete("/delete_notes/{note_id}")
async def delete_note(
    note_id: str,
    current_user: dict = Depends(get_current_user),
):
    if current_user["role"] != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )

    result = notes_collection.delete_one(
        {"_id": ObjectId(note_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    return {"message": "Note deleted successfully"}
