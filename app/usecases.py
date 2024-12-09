from app.repositories import CareerRepository
from app.domain import Career
from app.results import (
    CreateCareerResult,
    ListCareersResult,
    UpdateCareerResult,
    DeleteCareerResult,
)


class CreateCareerUseCase:
    repository = CareerRepository()

    def __init__(self, career: Career):
        self.__career = career

    def run(self):
        career = self.repository.save_career(self.__career)

        if career:
            return CreateCareerResult("success", career)

        return CreateCareerResult("failure")


class ListCareerUseCase:
    repository = CareerRepository()

    def run(self) -> ListCareersResult:
        career_list = self.repository.list_careers()

        if career_list is not None:
            return ListCareersResult("success", career_list)

        return ListCareersResult("failure")


class UpdataCareerUseCase:
    repository = CareerRepository()

    def __init__(self, career: Career):
        self.__career = career

    def run(self) -> UpdateCareerResult:
        career = self.repository.update_career(self.__career)

        if not career:
            return UpdateCareerResult("failure")

        if not hasattr(career, "id"):
            return UpdateCareerResult("failure", career)

        return UpdateCareerResult("success", career)


class DeleteCareerUseCase:
    repository = CareerRepository()

    def run(self, id: int) -> DeleteCareerResult:
        career = self.repository.get_career_by_id(id)

        if career is None:
            return DeleteCareerResult("failure")

        if not hasattr(career, "id"):
            return DeleteCareerResult("failure", career)

        id = self.repository.delete_career(career)

        if id is None:
            return DeleteCareerResult("failure")

        return DeleteCareerResult("success")
