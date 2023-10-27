from fastapi import File, UploadFile,Depends,APIRouter,BackgroundTasks
import logging
import aiofiles
from pathlib import Path
from auth.permissions import AuthHandler
from auth.user import get_current_user
from constants import *
from model import final_result,load_llm
from ingest import create_vector_db


logger = logging.getLogger()

auth_handler = AuthHandler()
router = APIRouter(
    prefix="/llm2",
    tags=['AiChat']
)





@router.get("/download-llm/")
async def download_llm_model(user=Depends(get_current_user)):
    llm_model= load_llm()

    return llm_model


@router.post("/upload")
async def upload_files(background_tasks: BackgroundTasks,files: list[UploadFile] = File(...),user=Depends(get_current_user)):
    filenames = []
    for file in files:
        # Create the file path
        data_folder = Path(SOURCE_DIRECTORY)
        destination_file_path = data_folder/file.filename
        async with aiofiles.open(destination_file_path, 'wb') as out_file:
            while content := await file.read(1024):
                await out_file.write(content)
        filenames.append(file.filename)
        background_tasks.add_task(create_vector_db)

    return {"filenames": filenames, "message": "Files uploaded successfully"}

@router.get("/chat/")
async def ai_chat(user_question: str,user=Depends(get_current_user)):
    msg=final_result(user_question)

    return msg




# Error handler for session verification failures
# @router.exception_handler(HTTPException)
# async def session_verification_exception_handler(request, exc):
#     logging.error(f"Session verification failed: {exc}")
#     return {"detail": "Internal failure of session verification"}



# poetry run uvicorn --port 8001 main:app --reload

# @app.post("/create_session/{name}")
# async def create_session(name: str, response: Response):
#
#     session = uuid4()
#     data = SessionData(username=name)
#
#     await backend.create(session, data)
#     print(response.body)
#     cookie.attach_to_response(response, session)
#
#     return f"created session for {name}"


# @app.get("/whoami", dependencies=[Depends(cookie)])
# async def whoami(session_data: SessionData = Depends(verifier)):
#     return session_data
#
#
# @app.post("/delete_session")
# async def del_session(response: Response, session_id: UUID = Depends(cookie)):
#     await backend.delete(session_id)
#     cookie.delete_from_response(response)
#     return "deleted session"
