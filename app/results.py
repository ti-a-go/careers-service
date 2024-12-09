from typing import Optional

from app.domain import Career


class CreateCareerResult:

    def __init__(
        self,
        name: str,
        career: Optional[Career] = None,
    ):
        self.name = name
        if career:
            self.career = career


class ListCareersResult:

    def __init__(
        self,
        name: str,
        career_list: Optional[list[Career]] = None,
    ):
        self.name = name

        if career_list is not None:
            self.career_list = career_list


class UpdateCareerResult:

    def __init__(
        self,
        name: str,
        career: Optional[Career] = None,
    ):
        self.name = name

        if career:
            self.career = career


class DeleteCareerResult:

    def __init__(
        self,
        name: str,
        career: Optional[Career] = None,
    ):
        self.name = name

        if career:
            self.career = career
