from rest_framework import status

from app.results import (
    CreateCareerResult,
    ListCareersResult,
    UpdateCareerResult,
    DeleteCareerResult,
)
from app.serializers import (
    ListCareerSerializer,
    CreateCareerSerializer,
    UpdateCareerSerializer,
    DeleteCareerSerializer,
)


INTERNAL_SERVER_ERROR_DATA = {
    "error_essage": "Please, contact the server maintainers."
}
NOT_FOUND_DATA = {"error_message": "Career not found"}


class CreateCareerResponse:
    __serializer_class = CreateCareerSerializer

    def __init__(self, result: CreateCareerResult):
        self.__result = result

    @property
    def is_success(self) -> bool:
        if self.__result.name == "success":
            return True

        return False

    @property
    def data(self):
        if self.is_success:
            return self.__serializer_class(self.__result.career).data
        return INTERNAL_SERVER_ERROR_DATA

    @property
    def status(self):
        if self.is_success:
            return status.HTTP_201_CREATED
        return status.HTTP_500_INTERNAL_SERVER_ERROR


class ListCareersResponse:
    serializer_class = ListCareerSerializer

    def __init__(self, result: ListCareersResult):
        self.__result = result

    @property
    def data(self):
        if self.is_success:
            serializer = self.serializer_class(
                self.__result.career_list, many=True
            )
            return serializer.data
        return INTERNAL_SERVER_ERROR_DATA

    @property
    def status(self):
        if self.__result.name == "success":
            return status.HTTP_200_OK
        return status.HTTP_500_INTERNAL_SERVER_ERROR

    @property
    def is_success(self) -> bool:
        if self.__result.name == "success":
            return True

        return False


class UpdateCareerResponse:
    serializer_class = UpdateCareerSerializer

    def __init__(self, result: UpdateCareerResult):
        self.__result = result

    @property
    def is_success(self) -> bool:
        if self.__result.name == "success":
            return True

        return False

    @property
    def is_not_found(self) -> bool:
        if (
            self.__result.name == "failure" and
            hasattr(self.__result, "career") and
            not hasattr(self.__result.career, "id")
        ):
            return True

        return False

    @property
    def status(self):
        if self.is_success:
            return status.HTTP_200_OK

        if self.is_not_found:
            return status.HTTP_404_NOT_FOUND

        return status.HTTP_500_INTERNAL_SERVER_ERROR

    @property
    def data(self):
        if self.is_success:
            return self.serializer_class(self.__result.career).data

        if self.is_not_found:
            return NOT_FOUND_DATA

        return INTERNAL_SERVER_ERROR_DATA


class DeleteCareerResponse:
    serializer_class = DeleteCareerSerializer

    def __init__(self, result: DeleteCareerResult):
        self.__result = result

    @property
    def is_success(self) -> bool:
        if self.__result.name == "success":
            return True

        return False

    @property
    def is_not_found(self) -> bool:
        if (
            self.__result.name == "failure"
            and hasattr(self.__result, "career")
            and not hasattr(self.__result.career, "id")
        ):
            return True

        return False

    @property
    def status(self):
        if self.is_success:
            return status.HTTP_204_NO_CONTENT

        if self.is_not_found:
            return status.HTTP_404_NOT_FOUND

        return status.HTTP_500_INTERNAL_SERVER_ERROR

    @property
    def data(self):
        if self.is_success:
            return {}

        if self.is_not_found:
            return NOT_FOUND_DATA

        return INTERNAL_SERVER_ERROR_DATA
