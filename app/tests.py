import json
from datetime import datetime
import logging
from mock import patch
from django.db.models import QuerySet

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from app.models import CareerModel
from app.responses import INTERNAL_SERVER_ERROR_DATA, NOT_FOUND_DATA


logging.disable(logging.CRITICAL)


class CareerTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_should_list_all_careers(self):
        # Given
        username = "username"
        title = "title"
        content = "content"

        CareerModel.objects.create(username=username, title=title, content=content)

        # When
        response = self.client.get("/careers/")

        # Then
        listed_careers = json.loads(response.content.decode())
        career = listed_careers[0]

        assert response.status_code == status.HTTP_200_OK

        assert len(listed_careers) == 1

        assert career["username"] == username
        assert career["title"] == title
        assert career["content"] == content
        assert career["id"] == 1
        assert type(career["created_datetime"]) == str

    def test_should_return_empy_career_list(self):
        # Given

        # When
        response = self.client.get("/careers/")

        # Then
        career_list = json.loads(response.content.decode())

        assert response.status_code == status.HTTP_200_OK

        assert len(career_list) == 0

    def test_should_not_list_all_careers_when_database_raises_exception(self):
        # Set up
        with patch.object(CareerModel.objects, "all") as mock_method:
            mock_method.side_effect = Exception("Test database raise exception.")

            # Given
            CareerModel.objects.create(
                username="username", title="title", content="content"
            )

            # When
            response = self.client.get("/careers/")

            # Then
            error_body = json.loads(response.content.decode())

            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert error_body == INTERNAL_SERVER_ERROR_DATA

    def test_should_create_new_career(self):
        # Given
        post_data = {"username": "username", "title": "title", "content": "content"}

        # When
        response = self.client.post("/careers/", post_data)

        # Then
        career: dict = json.loads(response.content.decode())
        created_career = CareerModel.objects.all()

        assert response.status_code == status.HTTP_201_CREATED

        assert career == post_data
        assert career.get("id") == None
        assert career.get("created_datetime") == None

        assert created_career[0].id == 1
        assert type(created_career[0].created_datetime) == datetime

    def test_should_not_create_career_when_database_raises_exception(self):
        # Set up
        with patch.object(CareerModel, "save") as mock_method:
            mock_method.side_effect = Exception("Test database raise exception.")

            # Given
            post_data = {"username": "username", "title": "title", "content": "content"}

            # When
            response = self.client.post("/careers/", post_data)

            # Then
            error_body: dict = json.loads(response.content.decode())

            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert error_body == INTERNAL_SERVER_ERROR_DATA

    def test_should_not_create_new_career_when_data_is_not_valid(self):
        # Given
        post_data = {}

        # When
        response = self.client.post("/careers/", post_data)

        # Then
        errors = json.loads(response.content.decode())

        expected_errors = {
            "username": ["This field is required."],
            "title": ["This field is required."],
            "content": ["This field is required."],
        }

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert errors == expected_errors

    def test_should_update_career(self):
        # Set up
        username = "username"
        CareerModel.objects.create(username=username, title="title", content="content")

        # Given
        patch_data = {"title": "new title", "content": "new content"}

        # When
        response = self.client.patch("/careers/1/", patch_data)

        # Then
        updated_career = CareerModel.objects.filter(id=1).first()
        response_data = json.loads(response.content.decode())

        assert response_data == patch_data
        assert response.status_code == status.HTTP_200_OK

        assert updated_career.id == 1
        assert updated_career.username == username
        assert updated_career.title == patch_data["title"]
        assert updated_career.content == patch_data["content"]

    def test_should_not_update_career_when_database_raises_exception_while_search_career(
        self,
    ):
        # Set up
        with patch.object(CareerModel.objects, "filter") as mock_method:
            mock_method.side_effect = Exception("Test database raise exception.")

            username = "username"
            CareerModel.objects.create(
                username=username, title="title", content="content"
            )

            # Given
            patch_data = {"title": "new title", "content": "new content"}

            # When
            response = self.client.patch("/careers/1/", patch_data)

            # Then
            error_body = json.loads(response.content.decode())

            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert error_body == INTERNAL_SERVER_ERROR_DATA

    def test_should_not_update_career_when_database_raises_exception_while_updating_career(
        self,
    ):
        # Set up
        with patch.object(QuerySet, "update") as mock_method:
            mock_method.side_effect = Exception("Test database raise exception.")

            username = "username"
            CareerModel.objects.create(
                username=username, title="title", content="content"
            )

            # Given
            patch_data = {"title": "new title", "content": "new content"}

            # When
            response = self.client.patch("/careers/1/", patch_data)

            # Then
            error_body = json.loads(response.content.decode())

            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert error_body == INTERNAL_SERVER_ERROR_DATA

    def test_should_not_update_career_when_request_data_is_not_valid(self):
        # Set up
        career_data = {
            "id": 1,
            "username": "username",
            "title": "title",
            "content": "content",
        }
        CareerModel.objects.create(
            username=career_data["username"],
            title=career_data["title"],
            content=career_data["content"],
        )

        # Given
        patch_data = {}

        # When
        response = self.client.patch(f"/careers/{career_data['id']}/", patch_data)

        # Then
        career = CareerModel.objects.filter(id=career_data["id"]).first()
        response_data = json.loads(response.content.decode())
        expected_response_data = {
            "title": ["This field is required."],
            "content": ["This field is required."],
        }

        assert response_data == expected_response_data
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert career.id == career_data["id"]
        assert career.username == career_data["username"]
        assert career.title == career_data["title"]
        assert career.content == career_data["content"]

    def test_should_not_update_career_when_career_is_not_found(self):
        # Set up
        career_data = {
            "id": 1,
            "username": "username",
            "title": "title",
            "content": "content",
        }
        CareerModel.objects.create(
            username=career_data["username"],
            title=career_data["title"],
            content=career_data["content"],
        )

        # Given
        not_existent_id = 2
        patch_data = {
            "username": "new username",
            "title": "new title",
            "content": "new content",
        }

        # When
        response = self.client.patch(f"/careers/{not_existent_id}/", patch_data)

        # Then
        career = CareerModel.objects.filter(id=career_data["id"]).first()
        response_data = json.loads(response.content.decode())

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response_data == NOT_FOUND_DATA

        assert career.id == career_data["id"]
        assert career.username == career_data["username"]
        assert career.title == career_data["title"]
        assert career.content == career_data["content"]

    def test_should_delete_career(self):
        # Given
        career_data = {
            "id": 1,
            "username": "username",
            "title": "title",
            "content": "content",
        }
        CareerModel.objects.create(
            username=career_data["username"],
            title=career_data["title"],
            content=career_data["content"],
        )

        # When
        response = self.client.delete(f"/careers/{career_data['id']}/")

        # Then
        career = CareerModel.objects.filter(id=career_data["id"]).first()
        response_data = response.content.decode()


        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response_data == ""

    def test_should_not_delete_career_when_it_is_not_found(self):
        # Given
        no_existent_id = 2
        career_data = {
            "id": 1,
            "username": "username",
            "title": "title",
            "content": "content",
        }
        CareerModel.objects.create(
            username=career_data["username"],
            title=career_data["title"],
            content=career_data["content"],
        )

        # When
        response = self.client.delete(f"/careers/{no_existent_id}/")

        # Then
        career = CareerModel.objects.filter(id=career_data["id"]).first()
        response_data = json.loads(response.content.decode())


        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response_data == NOT_FOUND_DATA

    def test_should_not_delete_career_when_database_raises_exception(self):
        # Set up
        with patch.object(QuerySet, "delete") as mock_method:
            mock_method.side_effect = Exception("Test database raise exception.")
            
            # Given
            career_data = {
                "id": 1,
                "username": "username",
                "title": "title",
                "content": "content",
            }
            CareerModel.objects.create(
                username=career_data["username"],
                title=career_data["title"],
                content=career_data["content"],
            )

            # When
            response = self.client.delete(f"/careers/{career_data['id']}/")

            # Then
            career = CareerModel.objects.filter(id=career_data["id"]).first()
            response_data = json.loads(response.content.decode())

            assert career.id == career_data["id"]
            assert career.username == career_data["username"]
            assert career.title == career_data["title"]
            assert career.content == career_data["content"]

            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert response_data == INTERNAL_SERVER_ERROR_DATA
    
    def test_should_not_delete_career_when_database_raises_exception_when_trying_to_get_career_by_id(self):
        # Set up
        with patch.object(CareerModel.objects, "filter") as mock_method:
            mock_method.side_effect = Exception("Test database raise exception.")
            
            # Given
            career_data = {
                "id": 1,
                "username": "username",
                "title": "title",
                "content": "content",
            }
            CareerModel.objects.create(
                username=career_data["username"],
                title=career_data["title"],
                content=career_data["content"],
            )

            # When
            response = self.client.delete(f"/careers/{career_data['id']}/")

            # Then
            response_data = json.loads(response.content.decode())

            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
            assert response_data == INTERNAL_SERVER_ERROR_DATA