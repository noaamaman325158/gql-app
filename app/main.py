from graphene import Schema
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from app.db.database import prepare_database
from app.gql.queries import Query

schema = Schema(query=Query)

app = FastAPI()


@app.on_event("startup")
def startup_event():
    prepare_database()


app.mount("/graphql", GraphQLApp(
    schema=schema,
    on_get=make_graphiql_handler()
))
