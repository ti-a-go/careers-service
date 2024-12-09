import logging
from typing import Optional

from app.models import CareerModel
from app.domain import Career


logger = logging.getLogger(__name__)


class CareerRepository:

    def list_careers(self) -> Optional[list[Career]]:
        try:
            query_set = CareerModel.objects.all()

        except Exception as e:
            logger.error("Failed to retreive Careers from database", str(e))
            return None

        careers = [
            Career(
                id=career_model.id,
                created_datetime=career_model.created_datetime,
                username=career_model.username,
                title=career_model.title,
                content=career_model.content,
            )
            for career_model in query_set
        ]

        return careers

    def save_career(self, career: Career) -> Optional[Career]:
        career_model = CareerModel(
            username=career.username, title=career.title, content=career.content
        )

        try:
            career_model.save()

        except Exception as e:
            logger.error(
                f"Failed to create a Career in the database. {str(career)}. {str(e)}"
            )
            return None

        return career

    def update_career(self, career: Career) -> Optional[Career]:
        try:
            found_career = CareerModel.objects.filter(id=career.id)
        except Exception as e:
            logger.error(
                f"An exception happened while trying to find the career with id: {career.id}. Exception: {str(e)}"
            )
            return None

        if not found_career:
            logger.error(f"Could not find any career with id: {career.id}")
            return Career.create_empty_career()

        try:
            found_career.update(title=career.title, content=career.content)
        except Exception as e:
            logger.error(
                f"An exception happened while trying to update the career with id: {career.id}. Exception: {str(e)}"
            )
            return None

        return career


    def delete_career(self, career: Career) -> Optional[int]:
        try:
            CareerModel.objects.filter(id=career.id).delete()
        except Exception as e:
            logger.error(
                f"An exception happened when trying to delete Career with id: {id}. Exception: {e}"
            )
            return None

        logger.info(f"Career delete successfully. Id: {id}")
        return id
    

    def get_career_by_id(self, id: int) -> Optional[Career]:
        try:
            found_career = CareerModel.objects.filter(id=id).first()
        
        except Exception as e:
            logger.error(
                f"An exception happened while trying to find the career with id: {id}. Exception: {str(e)}"
            )
            return None

        if not found_career:
            logger.error(f"Could not find any career with id: {id}")
            return Career.create_empty_career()

        logger.info(f"Found Career with id: {id}")
        return Career(
            id=found_career.id,
            created_datetime=found_career.created_datetime,
            username=found_career.username,
            title=found_career.title,
            content=found_career.content,
        )
