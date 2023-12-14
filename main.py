from graphene import Schema, ObjectType, String, Int, List, Field
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_graphiql_handler


class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject)


class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)


class Query(ObjectType):
    pass


schema = Schema(query=Query)

app = FastAPI()

app.mount("/graphql", GraphQLApp(
    schema=schema,
    on_get=make_graphiql_handler()
))
