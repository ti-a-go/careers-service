from datetime import datetime
from typing import Optional


class Career:

    def __init__(
        self,
        title: str,
        content: str,
        username: Optional[str] = None,
        id: Optional[int] = None,
        created_datetime: Optional[datetime] = None,
    ):
        self.title = title
        self.content = content

        if username:
            self.username = username
        if id:
            self.id = id
        if created_datetime:
            self.created_datetime = created_datetime

    @staticmethod
    def create_empty_career():
        return Career(username="", title="", content="")
