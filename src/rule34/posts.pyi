from _typeshed import Incomplete
from dataclasses import dataclass, field
from enum import Enum
from pydantic import BaseModel, Field as Field, model_validator as model_validator

class Rating(Enum):
    EXPLICIT = 0
    QUESTIONABLE = 1
    SAFE = 2
    @classmethod
    def from_string(cls, value: str): ...

@dataclass
class TagInfo:
    count: dict[str, int] = field(default_factory=dict)
    general: set[str] = field(default_factory=set)
    meta: set[str] = field(default_factory=set)
    artists: set[str] = field(default_factory=set)
    characters: set[str] = field(default_factory=set)
    copyrights: set[str] = field(default_factory=set)
    @classmethod
    def from_json(cls, tag_info: list[dict]) -> TagInfo: ...

class Post(BaseModel):
    height: int
    score: int
    file_url: str
    parent_id: int
    sample_url: str
    sample_width: int
    sample_height: int
    preview_url: str
    rating: Rating
    tags: set[str]
    post_id: int
    width: int
    change: int
    post_hash: str
    owner: str
    status: str
    source: str
    has_notes: bool
    comment_count: int
    post_json: str | None
    tag_info: TagInfo | None
    model_config: Incomplete
    @classmethod
    def from_json(cls, post_json: str) -> Post: ...
    @classmethod
    def from_multiple_json(cls, posts_json: str) -> list['Post']: ...
