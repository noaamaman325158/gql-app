from graphene import Schema, ObjectType, String, Int, List, Field
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from sqlalchemy import create_engine


# Here I paste postgres connection string
DB_URL = "DB_URL"
engine = create_engine(DB_URL)
conn = engine.connect()

# Static Data
employers_data = [
    {"id": 1, "name": "MetaTechA", "contact_email": "contact@company-a.com", "industry": "Tech"},
    {"id": 2, "name": "MoneySoftB", "contact_email": "contact@company-b.com", "industry": "Finance"},
]

jobs_data = [
    {"id": 1, "title": "Software Engineer", "description": "Develop web applications", "employer_id": 1},
    {"id": 2, "title": "Data Analyst", "description": "Analyze data and create reports", "employer_id": 1},
    {"id": 3, "title": "Accountant", "description": "Manage financial records", "employer_id": 2},
    {"id": 4, "title": "Manager", "description": "Manage people who manage records", "employer_id": 2},
]


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


class Query(ObjectType):
    jobs = List(JobObject)
    employers = List(EmployerObject)

    @staticmethod
    def resolve_jobs(root, info):
        return jobs_data

    @staticmethod
    def resolve_employers(root, info):
        return employers_data


schema = Schema(query=Query)

app = FastAPI()

app.mount("/graphql", GraphQLApp(
    schema=schema,
    on_get=make_graphiql_handler()
))
