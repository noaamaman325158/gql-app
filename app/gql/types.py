from graphene import ObjectType, String, Int, List, Field

class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject)

    @staticmethod
    def resolve_jobs(root, info):
        # Correct the key from "employer_data" to "employer_id"
        return [job for job in jobs_data if job["employer_id"] == root["id"]]


class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)

    @staticmethod
    def resolve_employers(root, info):
        # Using generator expression for getting only one value
        return next((employer for employer in employers_data if employer["id"] == root["employer_id"]), None)
