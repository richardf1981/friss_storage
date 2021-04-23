#
# This is controller which provides Endpoints for
# file operations: upload/download etc
#
from fastapi import APIRouter, Depends
from fastapi import File, UploadFile, HTTPException
from starlette.responses import FileResponse

from ..config import get_settings
from ..datalayer.db import SessionLocal
from ..dependencies import fastapi_users, class_file_manager
from ..services.exception_filemanager import FileAlreadyExistsError, \
    FilePhysicalDbNotFoundError

router = APIRouter(
    prefix="/api",
    responses={404: {"description": "Not found"}},
    tags=["api"]
)

file_manager_obj = class_file_manager(SessionLocal())
file_manager_obj.set_path(get_settings().path_media_file)


@router.post("/v1/file_upload")
async def file_upload(file: UploadFile = File(...),
                      user=Depends(fastapi_users.get_current_active_user)):
    try:
        file_manager_obj.upload(file, file.file, user.id)
    except FileAlreadyExistsError:
        raise HTTPException(status_code=400, detail="File already exists")
    except FilePhysicalDbNotFoundError:
        raise HTTPException(status_code=400,
                            detail="Internal error: Physical file not found")

    return {"status": "done"}


@router.put("/v1/file_upload")
@router.patch("/v1/file_upload")
async def file_upload_replace(file: UploadFile = File(...),
                              user=Depends(
                                  fastapi_users.get_current_active_user)):
    if not file_manager_obj.exists_file(file.filename):
        raise HTTPException(status_code=404,
                            detail="File not found, unable to replace")

    try:
        file_manager_obj.upload(file, file.file, user.id, True)
    except FilePhysicalDbNotFoundError:
        raise HTTPException(status_code=404,
                            detail="File not found, unable to replace")

    return {"status": "done"}


@router.get("/v1/file_download",
            responses={200: {"description": "File content for download"}})
async def file_download(file_name: str,
                        user=Depends(fastapi_users.get_current_active_user)):
    try:
        full_path, mime_type = file_manager_obj. \
            download_file(file_name, user.id)
    except FilePhysicalDbNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

    if get_settings().type == "file_system":
        return FileResponse(full_path,
                            media_type=mime_type,
                            filename=file_name)

    return HTTPException(status_code=500,
                         detail="Internal configuration error")
