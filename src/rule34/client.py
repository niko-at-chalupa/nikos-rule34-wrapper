import shlex
import requests
from .posts import Post
from pathlib import Path
import magic
import time

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

if __name__ == "__main__":
    from time import perf_counter
    from dotenv import load_dotenv
    import os
    start = perf_counter()
    load_dotenv()
    client = Client(os.environ["API_KEY"], os.environ["USER_ID"])
    tags = input("Search (limit of 200 posts will be fetched): ")

    try:
        from rich.console import Console # type:ignore
        from rich.progress import Progress, SpinnerColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn # type:ignore
        _rich = True
        console = Console()
    except ImportError:
        _rich = False

    if _rich:
        with Progress(SpinnerColumn(), "[progress.description]{task.description}", transient=True, console=console) as progress:
            progress.add_task("Fetching posts...", total=None)
            posts = client.list_posts(tags=tags, limit=200)
    else:
        print("Fetching posts...")
        posts = client.list_posts(tags=tags, limit=200)

    print(f"took {perf_counter() - start}s")

    for post in posts:
        print(f"FILE URL: {post.file_url}")
        print(f"ID: {post.post_id}\nPARENT ID: {post.parent_id}")
        print(str(post.tag_info) + "\n---")

    def download_posts(posts: list[Post], destination: Path) -> None:
        if _rich:
            with Progress(
                "[progress.description]{task.description}",
                BarColumn(),
                TaskProgressColumn(),
                TimeElapsedColumn(),
                console=console,
            ) as progress:
                task = progress.add_task("Downloading...", total=len(posts))
                for post in posts:
                    client.download_post(post=post, destination=destination)
                    progress.advance(task)
                    progress.console.print(f"Downloaded post {str(post.post_id)}")
        else:
            for post in posts:
                client.download_post(post=post, destination=destination)
                print(f"Downloaded post {str(post.post_id)}")

    print(f"{len(posts)} posts")

    while True:
        inputted = input("Download? (y/n) ")
        if inputted.lower() == "y":
            download_posts(posts=posts, destination=Path(input("Destination: ")))
            print("Finished!!")
            exit()
            exit()
            exit()
        elif inputted.lower() == "n":
            exit()