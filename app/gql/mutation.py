from graphene import Mutation, String, Int, Field, ObjectType
from app.gql.types import JobObject
from app.db.database import Session
from app.db.models import Job


class AddJob(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        employer_id = Int(required=True)

    job = Field(lambda: JobObject)

    @staticmethod
    def mutate(root, info, title, description, employer_id):
        job = Job(title=title, description=description, employer_id=employer_id)
        session = Session()
        session.add(job)
        session.commit()
        session.refresh(job)
        return AddJob(job=job)


class Mutation(ObjectType):
    add_job = AddJob.Field()