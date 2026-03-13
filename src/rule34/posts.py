import json
from enum import Enum
from dataclasses import dataclass, field

class Rating(Enum):
    EXPLICIT = 0
    QUESTIONABLE = 1
    SAFE = 2

    @classmethod
    def from_string(cls, value: str):
        if value == "e" or value == "explicit":
            return cls.EXPLICIT
        elif value == "q" or value == "questionable":
            return cls.QUESTIONABLE
        elif value == "s" or value == "safe":
            return cls.SAFE
        else:
            raise ValueError("Value passed into from_shorthand isn't valid!!")

@dataclass
class TagInfo:
    """
    Catagorizes tags.

    # Attributes
    ---
    general : set[str]
        General tags that don't belong in any other catagory. Most tags *(like "futanari")* fall under this.
    meta : set[str]
        Tags that describe special properties of a post, like if they have sound, or their resolution.
        Examples include:
            - sound
            - mp4
            - video
            - large_filesize
            - 3d
    artists : set[str]
        Tags that identify the original creator of a post's media.
    characters : set[str]
        Tags that identify named characters within a post.
    copyrights : set[str]
        Tags that identify the source franchise, series, or original work that the post's media is derived from, or associated with.
        Examples include:
            - vocaloid
            - utau
            - doki_doki_literature_club
            - monitoring_(deco*27)
    """
    general: set[str] = field(default_factory=set)
    meta: set[str] = field(default_factory=set)
    artists: set[str] = field(default_factory=set)
    characters: set[str] = field(default_factory=set)
    copyrights: set[str] = field(default_factory=set)

    @classmethod
    def from_json(cls, tag_info: list[dict]) -> "TagInfo":
        result = cls()
        for entry in tag_info:
            match entry["type"]:
                case "tag":      result.general.add(entry["tag"])
                case "metadata": result.meta.add(entry["tag"])
                case "artist":   result.artists.add(entry["tag"])
                case "character":result.characters.add(entry["tag"])
                case "copyrights":result.copyrights.add(entry["tag"])
        return result
    
    def __str__(self) -> str:
        lines = [f"{self.__class__.__name__}:"]
        for field_name, values in self.__dict__.items():
            lines.append(f"  {field_name}:")
            for value in sorted(values):
                lines.append(f"    - {value}")
        return "\n".join(lines)

class Post:
    """
    Represents a post on rule34.xxx.

    # Properties
    ---
    height : int
        Height of the post's media.
    score : int
        Defined by how many people voted "up" on the post.
    file_url : str
        URL to the post's media.
    parent_id : int
        Unique ID to a parent post *(if any)*.
        If `0`, then it is a top level post *(no parent)*.
    sample_url : str
        URL to a compressed version of the post's media. 
        Identical to the post's `file_url` if the media is small.
        If the post's media is a video, then this is a still image from that video.
    sample_width : int
        Defined by the width of the sample image *(the image from `sample_url`)*.
    sample_height : int
        Defined by the height of the sample image *(the image from `sample_url`)*.
    preview_url : str
        URL to a super small image of the media.
    rating : Rating
        The post's rating.
    tags : set[str]
        The post's tags.
    post_id : int
        The unique ID to identify the post.
    witdh : int
        Width of the post's media.
    change : int
        Unix timestamp to when was the last change to the post.
    hash : str
        I have no clue what defines this. I tried the md5 of the post's media, but it doesn't match up with the hash given to us by the API.
    owner : str
        Defined by the username of the uploader.
    status : str
        The post's status.
        This can be "active", "deleted", or something else. I have not found anything other than the two in my testing, but the fact it's a string and not a boolean leads me to believe there are more possible values.
    source : str
        URL to a source.
    has_notes : bool
        Weather if notes are attached to the post.
        Notes are things that get overlayed on top of a post's media, shown as transparent white boxes on the site.
    comment_count : int
        Defined by how many comments are on the post.
    post_json : str | None
        Raw JSON from the response used to get information about the post.
    tag_info : TagInfo | None
        Tags represented by a TagInfo object.
    """
    def __init__(
        self,
        height: int,
        score: int,
        file_url: str,
        parent_id: int,
        sample_url: str,
        sample_width: int,
        sample_height: int,
        preview_url: str,
        rating: Rating,
        tags: set[str],
        post_id: int,
        width: int,
        change: int,
        hash: str,
        owner: str,
        status: str, # I don't know the possibilities (I'm sorry!!!), and I don't know where I can find the posts that aren't "active". I won't make an enum for this, and this should be good enough anyways.
        # Update: looks like it's either "active" or "deleted". What's confusing me is that it isn't a boolean, but it not being a boolean leads me to believe that there's other states (maybe 'pending')
        source: str,
        has_notes: bool,
        comment_count: int,
        post_json: str | None = None,
        tag_info: TagInfo | None = None
    ):
        self._height = height
        self._score = score
        self._file_url = file_url
        self._parent_id = parent_id
        self._sample_url = sample_url
        self._sample_width = sample_width
        self._sample_height = sample_height
        self._preview_url = preview_url
        self._rating = rating
        self._tags = tags
        self._post_id = post_id
        self._width = width
        self._change = change
        self._hash = hash
        self._owner = owner
        self._status = status
        self._source = source
        self._has_notes = has_notes
        self._comment_count = comment_count
        self._post_json = post_json
        self._tag_info = tag_info
        # I don't want to type all of this ever again

    @property
    def height(self) -> int:
        return self._height

    @property
    def score(self) -> int:
        return self._score

    @property
    def file_url(self) -> str:
        return self._file_url

    @property
    def parent_id(self) -> int:
        return self._parent_id

    @property
    def sample_url(self) -> str:
        return self._sample_url

    @property
    def sample_width(self) -> int:
        return self._sample_width

    @property
    def sample_height(self) -> int:
        return self._sample_height

    @property
    def preview_url(self) -> str:
        return self._preview_url

    @property
    def rating(self) -> Rating:
        return self._rating

    @property
    def tags(self) -> set[str]:
        return self._tags

    @property
    def post_id(self) -> int:
        return self._post_id

    @property
    def width(self) -> int:
        return self._width

    @property
    def change(self) -> int:
        return self._change

    @property
    def hash(self) -> str:
        return self._hash

    @property
    def owner(self) -> str:
        return self._owner

    @property
    def status(self) -> str:
        return self._status

    @property
    def source(self) -> str:
        return self._source

    @property
    def has_notes(self) -> bool:
        return self._has_notes

    @property
    def comment_count(self) -> int:
        return self._comment_count

    @property
    def post_json(self) -> str | None:
        return self._post_json

    @property
    def tag_info(self) -> TagInfo | None:
        return self._tag_info

    @classmethod
    def from_json(cls, post_json: str):
        d = json.loads(post_json)
        if isinstance(d, list):
            if len(d) != 1:
                raise ValueError(f"Expected a single post object, got a list of {len(d)}. Use Post.many_from_json() instead.")
            d = d[0]
        return cls(
            height=d["height"],
            score=d["score"],
            file_url=d["file_url"],
            parent_id=d["parent_id"],
            sample_url=d["sample_url"],
            sample_width=d["sample_width"],
            sample_height=d["sample_height"],
            preview_url=d["preview_url"],
            rating=Rating.from_string(d["rating"]),
            tags=set(d["tags"].split()),
            post_id=d["id"],
            width=d["width"],
            change=d["change"],
            hash=d["hash"],
            owner=d["owner"],
            status=d["status"],
            source=d.get("source", ""),
            has_notes=d["has_notes"],
            comment_count=d["comment_count"],
            post_json=post_json,
            tag_info=TagInfo.from_json(d["tag_info"]) if "tag_info" in d else None,
        )

    @classmethod
    def from_multiple_json(cls, posts_json: str) -> list["Post"]:
        d = json.loads(posts_json)
        if not isinstance(d, list):
            d = [d]
        return [cls.from_json(json.dumps(post)) for post in d]