from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.models.notes import Note
from app.schemas.notes import NoteCreate,NoteUpdate
from database import get_db
from summarizer import generate_summary


router = APIRouter(prefix="/notes")



@router.get("/get_note/{id}")
def get_specific_note(id:int,db:Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note Not Found")
    
    try:
        result = {
            "title":note.title,
            "content":note.content,
            "summary":note.summary
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error While Getting Note")
        



@router.get("/get_all_notes")
def get_all_notes(db:Session=Depends(get_db)):
    try:
        notes = db.query(Note).all()

        return {"data":notes}
    except Exception as e:
        raise HTTPException(status_code=500,detail="Error While Getting Notes")




@router.post("/create_notes")
async def create_notes(payload:NoteCreate,db:Session = Depends(get_db)):
    try:
        summary = await generate_summary(payload.title)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
    
    try:
        print(f"Payload => {payload}")
        notes = Note(
            title = payload.title,
            content = payload.content,
            summary = summary
        )

        db.add(notes)
        db.commit()
        db.refresh(notes)

        return {"message":"Notes Created Succcessfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error on Creating Notes {e}")
        



@router.put("/update_note/{id}")
def update_specific_note(id:int,payload:NoteUpdate,db:Session=Depends(get_db)):
    note = db.query(Note).filter(Note.id == id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note Not Found")
    try:
        if payload.title != None:
            note.title = payload.title
        
        if payload.content != None:
            note.title = payload.content
        
        db.commit()
        db.refresh(note)
        return {"message":"Note Updated Successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error While Updating Note")



@router.delete("/delete_note/{id}")
def delete_specific_note(id:int,db:Session=Depends(get_db)):
    note = db.query(Note).filter(Note.id == id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note Not Found")
    try:
        db.delete(note)
        db.commit()
        return {"message":"Note Deleted Successfully"}
    except Exception as e:
        raise HTTPException(status_code=500,detail="Error While Deleting Notes ")