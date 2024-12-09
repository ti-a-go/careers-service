import logging

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from app.usecases import (
    ListCareerUseCase,
    CreateCareerUseCase,
    UpdataCareerUseCase,
    DeleteCareerUseCase,
)
from app.app_requests import CreateCareerRequest, UpdateCareerRequest
from app.responses import (
    ListCareersResponse,
    CreateCareerResponse,
    UpdateCareerResponse,
    DeleteCareerResponse,
)


logger = logging.getLogger(__name__)


class ListCreateCareerView(APIView):
    """
    View to list and create Carrers
    """

    def get(self, req: Request):
        """
        Method to list all Careers
        """
        logger.info("Starting list careers...")
        
        usecase = ListCareerUseCase()

        result = usecase.run()

        response = ListCareersResponse(result)

        if response.is_success:

            logger.info("Career list retreived successfully.")

            return Response(response.data, response.status)

        logger.error(
            f"Error when trying to list all Careers. {str(req)}. {str(response.data)}"
        )

        return Response(response.data, response.status)

    def post(self, req: Request):
        """
        Method to create a Career
        """
        request = CreateCareerRequest(req)

        if not request.is_data_valid():
            errors = request.validation_error_messages

            logger.error(f"Data validation error {str(errors)}")

            return Response(errors, request.status)

        usecase = CreateCareerUseCase(request.career_to_be_created)

        result = usecase.run()

        response = CreateCareerResponse(result)

        if response.is_success:
            logger.info("Career created successfully.", str(response.data))

            return Response(response.data, response.status)

        logger.error(
            f"Error while trying to create a new Career: {str(response.data)}"
        )

        return Response(response.data, response.status)


class UpdateDeleteCareerView(APIView):
    """
    View to update or delete a Career
    """

    def patch(self, req: Request, pk: str) -> Response:
        request = UpdateCareerRequest(req, pk)

        if not request.is_data_valid():
            logger.error(
                f"Data validation error: {str(request.validation_error_messages)}"
            )

            return Response(request.validation_error_messages, request.status)

        usecase = UpdataCareerUseCase(request.career_to_be_updated)

        result = usecase.run()

        response = UpdateCareerResponse(result)

        if response.is_success:
            logger.info(f"Career updated successfully. Id: {pk}")

            return Response(response.data, response.status)

        if response.is_not_found:
            logger.info(f"Could not find career to be update with id: {pk}")

            return Response(response.data, response.status)

        logger.error(f"Error while trying to update career with id: {pk}")

        return Response(response.data, response.status)

    def delete(self, req: Request, pk: str) -> Response:
        usecase = DeleteCareerUseCase()

        result = usecase.run(pk)

        response = DeleteCareerResponse(result)

        if response.is_success:
            logger.info(f"Career deleted successfully. Id: {pk}")

            return Response(response.data, response.status)

        if response.is_not_found:
            logger.info(f"Could not find career to be deleted with id: {pk}")

            return Response(response.data, response.status)

        logger.error(f"Error while trying to delete career with id: {pk}")

        return Response(response.data, response.status)
