from rest_framework.request import Request
from rest_framework import status

from app.serializers import CreateCareerSerializer, UpdateCareerSerializer
from app.domain import Career


class CreateCareerRequest:
    serializer_class = CreateCareerSerializer

    def __init__(self, request: Request):
        self.request = request

    def is_data_valid(self):
        self.serializer = self.serializer_class(data=self.request.data)
        return self.serializer.is_valid()

    @property
    def validation_error_messages(self):
        return self.serializer.errors

    @property
    def status(self):
        if not self.is_data_valid():
            return status.HTTP_400_BAD_REQUEST

    @property
    def career_to_be_created(self) -> Career:
        return Career(
            username=self.serializer.validated_data["username"],
            title=self.serializer.validated_data["title"],
            content=self.serializer.validated_data["content"],
        )


class UpdateCareerRequest:
    serializer_class = UpdateCareerSerializer

    def __init__(self, request: Request, id: int):
        self.request = request
        self.id = id

    def is_data_valid(self):
        self.serializer = self.serializer_class(data=self.request.data)
        return self.serializer.is_valid()

    @property
    def validation_error_messages(self):
        return self.serializer.errors

    @property
    def status(self):
        if not self.is_data_valid():
            return status.HTTP_400_BAD_REQUEST

    @property
    def career_to_be_updated(self) -> Career:
        return Career(
            id=self.id,
            title=self.serializer.validated_data["title"],
            content=self.serializer.validated_data["content"],
        )
