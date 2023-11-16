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


def add_application_to_db(job_id, first_name, last_name, email, resume_path, resume_filename):
  with engine.connect() as conn:
      query = text(
          "INSERT INTO applications(job_id, first_name, last_name, email, resume_path, resume_filename) "
          "VALUES (:job_id, :first_name, :last_name, :email, :resume_path, :resume_filename)"
      )
      conn.execute(
          query,
          {
              'job_id': job_id,
              'first_name': first_name,
              'last_name': last_name,
              'email': email,
              'resume_path': resume_path,
              'resume_filename': resume_filename,
          }
      )



