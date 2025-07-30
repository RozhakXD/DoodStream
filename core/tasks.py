import asyncio
import time
import os
from celery import shared_task
from .services import DoodStreamService
from django.conf import settings

FILE_LIFETIME_SECONDS = 3600

@shared_task(bind=True)
def download_video_task(self, video_url: str):
    """
    Celery task to download a video from a given URL in the background.
    This task is asynchronous and uses the DoodStreamService.
    """
    self.update_state(state='PROGRESS', meta={'status': 'Memulai proses unduhan...'})

    service = DoodStreamService()
    try:
        filepath = asyncio.run(service.download_single_video(video_url))

        if filepath:
            return {'status': 'SUCCESS', 'filepath': filepath}
        else:
            return {'status': 'FAILURE', 'error': 'Tidak dapat mengunduh video. Cek log worker.'}
    except Exception as e:
        return {'status': 'FAILURE', 'error': str(e)}

@shared_task(bind=True)
def scrape_folder_task(self, folder_url: str):
    """
    Celery task to scrape a folder URL and return the list of videos.
    """
    self.update_state(state='PROGRESS', meta={'status': 'Mengumpulkan daftar video dari folder...'})
    service = DoodStreamService()
    try:
        video_list = asyncio.run(service.scrape_folder_page(folder_url))
        if video_list is not None:
            return {'status': 'SUCCESS', 'videos': video_list}
        else:
            return {'status': 'FAILURE', 'error': 'Gagal mengambil data dari folder.'}
    except Exception as e:
        return {'status': 'FAILURE', 'error': str(e)}

@shared_task
def cleanup_old_files():
    """
    A periodic task to clean up old downloaded files from the media directory.
    This task should be run by Celery Beat.
    """
    now = time.time()
    cleanup_count = 0

    media_dir = settings.MEDIA_ROOT

    print(f"Running cleanup task for directory: {media_dir}")

    try:
        for filename in os.listdir(media_dir):
            filepath = os.path.join(media_dir, filename)

            if os.path.isfile(filepath):
                file_mod_time = os.path.getmtime(filepath)

                if (now - file_mod_time) > FILE_LIFETIME_SECONDS:
                    print(f"Deleting old file: {filepath}")
                    os.remove(filepath)
                    cleanup_count += 1
        
        if cleanup_count > 0:
            return f"Cleanup complete. Deleted {cleanup_count} old files."
        else:
            return "No old files to delete."
    except FileNotFoundError:
        return f"Directory not found: {media_dir}. Skipping cleanup."
    except Exception as e:
        print(f"An error occurred during cleanup: {e}")
        return f"Cleanup failed with error: {e}"