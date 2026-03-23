<div align="center">

# Niko's Rule34 Wrapper
</div>

> [!WARNING]
> The service this pulls media from is an NSFW service!!

> [!IMPORTANT]
> This is still work in progress!! Bugs WILL show up!!

A python wrapper/downloader for rule34.xxx!!

## Features
> - **CLI Interface** -
> Command-line tool for searching and listing posts from rule34.xxx with customizable tags and limits.

> - **Unlimited Fetching** -
> Supports fetching unlimited posts by paginating through API results (bypasses the 1000-post per-request limit).

> - **Pool Support** -
> Fetch posts from specific pools. I don't know of any other wrappers/downloaders that support pools.

> - **`tag_info` support** -
> Supports rule34's tag info stuff. This means that tags can be catagorized by their type *(general, artist, character...)*.

## Installation

<details><summary>Prerequisites</summary>

- Python 3.8 or higher
- API key and user ID from [api.rule34.xxx](https://api.rule34.xxx/)

Optional for enhanced UI:
- rich

---
</details>

> [!NOTE]
> This will get uploaded on PyPi in the future!!

> [!NOTE]
> This *should* work on Windows. Otherwise, open an issue!

> Installation through GitHub:
> ```bash
> pip install git+https://github.com/niko-at-chalupa/nikos-rule34-wrapper
> ```

Tested on:
- Linux *(Ubuntu)*
- MacOS *(Tahoe)*
- Termux

## Usage

Run the CLI tool:

```bash
python -m rule34 --tags "-ai_generated -scat -3d kasane_teto" --limit 100 --download --destination /path/to/download/
```

### Arguments
- `--tags` *(optional)*: Search tags *(e.g., "vocaloid", "sort:score", "-ai_generated")*. One of --tags, --pool-id, or --favorites-user-id must be specified.
- `--pool-id` *(optional)*: Pool ID to fetch posts from.
- `--favorites-user-id` *(optional)*: User ID to fetch favorites from.
- `--limit` *(optional)*: Number of posts to fetch *(default 200, 0 for unlimited)*.
- `--download` *(flag)*: Enable downloading of posts.
- `--destination` *(required if downloading)*: Path to save downloaded files.
- `--reset-credentials` *(flag)*: Prompt to re-enter API credentials.

### First Run
On first use, you'll be prompted for your API key and user ID. These are stored securely and reused in future runs.

### Examples
- List posts without downloading:
  ```bash
  python -m rule34 --tags "kasane_teto sort:score" --limit 50
  ```

- Download unlimited posts:
  ```bash
  python -m rule34 --tags "kasane_teto" --limit 0 --download --destination ./downloads # WILL download many files!!! It's okay to terminate with ctrl+C.
  ```

- Reset credentials:
  ```bash
  python -m rule34 --tags "kasane_teto sort:score" --reset-credentials --print-posts --taginfo # Will prompt for credentials before listing
  ```

- Fetch posts from a pool:
  ```bash
  python -m rule34 --pool-id 12345 --limit 50 --download --destination ./pool_downloads
  ```

- Fetch posts from user favorites:
  ```bash
  python -m rule34 --favorites-user-id 4525852 --limit 100
  ```

## API Reference

```python
from rule34 import Client

client = Client("your_api_key", "your_user_id")
posts = client.list_posts("kasane_teto", limit=100)
for post in posts:
    print(post.file_url)
```

See `client.py` for full method details.

## Contributing
Contributions are welcome!!! PLEASE open an issue or submit a pull request!!!

## Planned features
> - [ ] Httpx instead of requests

> - [ ] Async support

> - [x] PyPi package 
>
> Published at https://pypi.org/project/nikos-rule34-wrapper/!