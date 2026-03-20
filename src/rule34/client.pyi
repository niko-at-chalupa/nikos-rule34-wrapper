from .posts import Post as Post
from _typeshed import Incomplete
from pathlib import Path

logger: Incomplete
formatter: Incomplete
handler: Incomplete

class Client:
    API_KEY: Incomplete
    USER_ID: Incomplete
    def __init__(self, api_key: str, user_id: str) -> None: ...
    def list_posts(self, tags: str | set[str], limit: int = 1000, pid: int | None = None) -> list[Post]:
        '''
        List posts.

        # Parameters
        ---
        tags : str | set[str]
            The tags you want to search for while listing.
            This supports everything you could put in rule34.xxx\'s search, like "sort:score", "-ai_generated", and whatever else.
            Pass in an empty string or empty set to get everything.
        limit : int
            The limit of posts that will be returned. There is a hard limit of 1000 posts per request.
        pid : int | None
            The page number.
        '''
    def get_post(self, post_id: int) -> Post:
        """
        Get a post from its ID.

        # Parameters
        ---
        post_id : int
            The ID of the post you want to get.
        """
    def download_post(self, post: Post, destination: Path, file_name: str | None = None, file_url: str | None = None) -> None:
        """
        Download a post's media.

        # Parameters
        ---
        post : Post
            Post to download.
        destination : Path
            Directory to where the file will be saved.
        file_name : str | None
            Name for the file.
        file_url : str | None
            URL to download from. `None` will default to `post.file_url`.
            You can use stuff like `post.file_url`, `post.preview_url`, & `post.sample_url`.
        """
    def list_posts_from_pool(self, pool_id: int) -> list[Post]: ...
    def list_posts_from_favorites(self, user: int) -> list[Post]: ...
    def list_post_ids_from_pool(self, pool_id: int) -> list[int]: ...
    def list_post_ids_from_favorites(self, user: int) -> list[int]: ...
