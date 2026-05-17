import shutil

from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.services.images import ImagesService
from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображение отелей"])


@router.post("")
def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    ImagesService().upload_image(file, background_tasks)