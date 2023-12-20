from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, Employer, Job
from app.config.config import DB_URL
from app.db.data import employers_data, jobs_data

engine = create_engine(DB_URL)
conn = engine.connect()

Session = sessionmaker(bind=engine)


def prepare_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = Session()
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
    session.close()
