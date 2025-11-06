from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class CreateCommentParams:
    account_id: str
    task_id: str
    content: str

@dataclass(frozen=True)
class UpdateCommentParams:
    account_id: str
    comment_id: str
    content: str

@dataclass(frozen=True)
class DeleteCommentParams:
    account_id: str
    comment_id: str

@dataclass
class Comment:
    id: Optional[str]
    account_id: str
    task_id: str
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
