import asyncio
import aiohttp
import re
import random
import time
import os
from urllib.parse import urlparse, urljoin

class DoodStreamService:
    """
    A service class to handle all interactions with DoodStream,
    including fetching video links and downloading content.
    """

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        }
        self.output_dir = "downloaded_videos"
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def _get_final_media_url(self, session, embed_url: str) -> str | None:
        """
        Private helper method to extract the final, streamable media URL
        from a DoodStream embed page.
        """
        async with session.get(embed_url) as response:
            if response.status != 200:
                print(f"Error: Failed to access embed page {embed_url}, Status: {response.status}")
                return None
            
            text = await response.text()

            pass_md5_match = re.search(r'/pass_md5/([^"\']+)', text)
            if not pass_md5_match:
                print("Error: Could not find pass_md5 in page content.")
                return None
            
            pass_md5_path = pass_md5_match.group(1)
            domain = urlparse(embed_url).netloc
            pass_md5_url = f"https://{domain}/pass_md5/{pass_md5_path}"

            token = pass_md5_path.split('/')[-1]

            async with session.get(pass_md5_url) as md5_response:
                if md5_response.status != 200:
                    print(f"Error: Failed to get media URL from pass_md5 endpoint, Status: {md5_response.status}")
                    return None
                
                media_url_base = await md5_response.text()

                random_chars = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=10))
                final_url = f"{media_url_base}{random_chars}?token={token}&expiry={int(time.time())}"
                return final_url
    
    async def download_single_video(self, video_url: str) -> str | None:
        """
        Downloads a single video from a DoodStream URL (/d/ or /e/)
        and saves it to a local file.
        Returns the path to the downloaded file or None on failure.
        """
        embed_url = video_url.replace('/d/', '/e/')

        async with aiohttp.ClientSession(headers=self.headers) as session:
            session.headers.update({"Referer": embed_url})

            final_media_url = await self._get_final_media_url(session, embed_url)

            if not final_media_url:
                return None
            
            async with session.get(final_media_url) as video_response:
                if video_response.status not in [200, 206]:
                    print(f"Error: Failed to download video content, Status: {video_response.status}")
                    return None

                filename = f"dood_{int(time.time())}_{random.randint(100, 999)}.mp4"
                filepath = os.path.join(self.output_dir, filename)

                with open(filepath, 'wb') as f:
                    while True:
                        chunk = await video_response.content.read(1024 * 1024)  # Read in 1MB chunks
                        if not chunk:
                            break
                        f.write(chunk)
                
                print(f"Success: Video saved to {filepath}")
                return filepath

    async def scrape_folder_page(self, folder_url: str) -> list[dict] | None:
        """
        Scrapes a DoodStream folder page to get a list of all videos in it.
        Returns a list of dictionaries, each containing video details.
        """
        print(f"Scraping folder: {folder_url}")
        async with aiohttp.ClientSession(headers=self.headers) as session:
            session.headers.update({"Referer": folder_url})
            async with session.get(folder_url) as response:
                if response.status != 200:
                    print(f"Error: Failed to access folder page {folder_url}, Status: {response.status}")
                    return None

                text = await response.text()

                blocks = re.findall(
                    r'<h4>\s*(.*?)\s*</h4>.*?<span.*?>\s*(.*?)\s*</span>.*?<span.*?>\s*(.*?)\s*</span>.*?<span.*?>\s*(.*?)\s*</span>.*?<a[^>]+href="([^"]+)"[^>]*>.*?View.*?</a>',
                    text,
                    re.DOTALL
                )

                if not blocks:
                    print("No video blocks found on the folder page.")
                    return []

                videos = []
                for block in blocks:
                    raw_link = block[4].strip()
                    embed_link = urljoin(folder_url, raw_link).replace('/d/', '/e/')
                    
                    videos.append({
                        "title": block[0].strip(),
                        "size": block[1].strip(),
                        "duration": block[2].strip(),
                        "date": block[3].strip(),
                        "link": embed_link 
                    })
                return videos