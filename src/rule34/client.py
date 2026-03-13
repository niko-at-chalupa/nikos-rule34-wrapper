import requests
from .posts import Post

class Client:
    def __init__(self, api_key: str, user_id: str):
        self.API_KEY = api_key
        self.USER_ID = user_id

    def list_posts(self, tags: str | set[str], /, limit: int = 1000, pid: int | None = None) -> list[Post]:
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

if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    from time import perf_counter
    start = perf_counter()
    load_dotenv()
    client = Client(os.environ["API_KEY"], os.environ["USER_ID"])
    tags = input("input tags you want to search for: ")
    posts = client.list_posts(tags, limit=4)
    print(f"took {perf_counter() - start}s")
    for post in posts:
        print(f"FILE URL: {post.file_url}")
        print(str(post.tag_info) + "\n---")