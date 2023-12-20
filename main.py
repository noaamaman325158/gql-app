from graphene import Schema, ObjectType, String, Int, List, Field
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from sqlalchemy import create_engine, Column, Integer, String as saString, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Here I paste postgres connection string
DB_URL = "postgresql://postgres:2e54-cbD4-BbGbGDEDF--B555AGB33aF@viaduct.proxy.rlwy.net:31595/railway"
engine = create_engine(DB_URL)
conn = engine.connect()

Base = declarative_base()


# Define our entities in declarative python
class Employer(Base):
    __tablename__ = "employers"

    id = Column(Integer, primary_key=True)
    name = Column(saString)
    contact_email = Column(saString)
    industry = Column(saString)
    jobs = relationship("Job", back_populates="employer")


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    title = Column(saString)
    description = Column(saString)
    employer_id = Column(ForeignKey("employers.id"))
    employer = relationship("Employer", back_populates="jobs")


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# emp1 = Employer(id=1, name="noaa maman", contact_email="noaamaman325158@gmail.com", industry="Tech")
# session.add(emp1)
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

for employer in employers_data:
    # create a new instance of employer
    # emp = Employer(id=employer.get("id"), name=employer.get("name"), contact_email=employer.get("contact_email"),
    #                employer_id=employer.get("employer_id"))
    # add it to the session
    # **-> For unpacking the dictionary collection data structure type
    emp = Employer(**employer)
    session.add(emp)

for job in jobs_data:
    session.add(Job(**job))

session.commit()


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
