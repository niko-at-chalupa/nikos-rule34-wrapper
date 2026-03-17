import shlex
import requests
from .posts import Post
from pathlib import Path
import magic
import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

class Client:
    def __init__(self, api_key: str, user_id: str):
        self.API_KEY = api_key
        self.USER_ID = user_id

    def _add_extension(self, filepath: Path) -> Path:
        mime = magic.from_file(filepath, mime=True)
        mimetoext = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/gif": ".gif",
            "image/webp": ".webp",
            "image/bmp": ".bmp",
            "image/tiff": ".tiff",
            "image/svg+xml": ".svg",
            "image/avif": ".avif",
            "video/mp4": ".mp4",
            "video/quicktime": ".mov",
            "video/x-msvideo": ".avi",
            "video/x-matroska": ".mkv",
            "video/webm": ".webm",
            "video/mpeg": ".mpeg",
            "video/3gpp": ".3gp",
        }
        ext = mimetoext.get(mime)
        if not ext:
            raise ValueError(f"Unsupported or unrecognized MIME type: {mime}")
        new_path = filepath.with_suffix(filepath.suffix + ext)
        filepath.rename(new_path)
        return new_path

    def list_posts(self, tags: str | set[str], limit: int = 1000, pid: int | None = None) -> list[Post]:
        """
        List posts.

        # Paremeters
        ---
        tags : str | set[str]
            The tags you want to search for while listing.
            This supports everything you could put in rule34.xxx's search, like "sort:score", "-ai_generated", and whatever else.
            Pass in an empty string or empty set to get everything.
        limit : int
            The limit of posts that will be returned. There is a hard limit of 1000 posts per request.
        pid : int | None
            The page number.
        """
        params = {
            "page": "dapi",
            "s": "post",
            "q": "index",
            "api_key": self.API_KEY,
            "user_id": self.USER_ID,
            "fields": "tag_info",
            "json": "1",
            "limit": str(limit),
        }
        if pid is not None:
            params["pid"] = str(pid)
        if isinstance(tags, set):
            params["tags"] = " ".join(tags)
        else:
            params["tags"] = tags
        response = requests.get("https://api.rule34.xxx/index.php", params=params)
        if response.content.decode("utf-8") == "":
            return []
        return Post.from_multiple_json(response.content.decode("utf-8"))

    def get_post(self, post_id: int) -> Post:
        """
        Get a post from its ID.

        # Parameters
        ---
        post_id : int
            The ID of the post you want to get.
        """
        params = {
            "page": "dapi",
            "s": "post",
            "q": "index",
            "api_key": self.API_KEY,
            "user_id": self.USER_ID,
            "fields": "tag_info",
            "id": post_id,
            "json": "1"
        }
        response = requests.get("https://api.rule34.xxx/index.php", params=params)
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 5))
            time.sleep(retry_after)
            response = requests.get("https://api.rule34.xxx/index.php", params=params)
        response.raise_for_status()
        return Post.from_json(response.content.decode("utf-8"))
    
    def download_post(self, post: Post, destination: Path, file_name: str | None = None) -> None:
        response = requests.get(post.file_url, stream=True)
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 5))
            time.sleep(retry_after)
            response = requests.get(post.file_url, stream=True)
        response.raise_for_status()
        
        file_name2: str = str(post.post_id)
        if file_name:
            file_name2: str = str(file_name)
        elif destination.suffix: # A way to check if it leads to a file or not
            file_name2: str = destination.name
        
        destination2 = destination
        if destination.suffix: # A way to check if it leads to a file or not
            destination2 = destination.parent
        else:
            destination2 = destination
        if not destination2.exists:
            raise FileNotFoundError(f"{destination2} does NOT exist!")

        with Path(destination2 / file_name2).open("wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        self._add_extension(Path(destination2 / file_name2))

    def list_posts_from_pool(self, pool_id: int) -> list[Post]:
        def get_post_ids_from_html(html: str) -> list[int]:
            soup = BeautifulSoup(html, "lxml")
            post_ids = []
            for span in soup.find_all("span", id=lambda v: v and v.startswith("p")):
                try:
                    post_ids.append(int(span["id"][1:]))  # strip the leading "p"
                except ValueError:
                    continue
            return post_ids
        
        params = {
            "page": "pool",
            "s": "show",
            "id": pool_id
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }
        response = requests.get(f"https://rule34.xxx/index.php", params=params, headers=headers)
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 5))
            time.sleep(retry_after)
            response = requests.get(f"https://rule34.xxx/index.php", params=params, headers=headers)
        response.raise_for_status()
        html = response.content.decode("utf-8")
        post_ids = get_post_ids_from_html(html)
        
        posts = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(self.get_post, post_id=post): post for post in post_ids}
            for future in as_completed(futures):
                posts.append(future.result())

        return posts