import sqlalchemy
from sqlalchemy import create_engine, text
import os 

dbConnectionString = os.environ['DB_CONNECTION_STR']

engine = create_engine(dbConnectionString,
                       connect_args={"ssl": {
                           "ssl_ca": "/etc/ssl/cert.pem",
                       }})

def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM digitalboricareers.jobs"))
  
    jobs_list = []
    for row in result.all():
      jobs_list.append(row._mapping)
  
  return jobs_list

