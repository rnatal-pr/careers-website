from flask import Flask, jsonify, render_template, request, redirect, url_for
import os
from database import load_jobs_from_db, add_application_to_db

app = Flask(__name__)

# Set the path for the "Resumes" folder
RESUMES_FOLDER = os.path.join(os.getcwd(), 'Resumes')

# Create the "Resumes" folder if it doesn't exist
os.makedirs(RESUMES_FOLDER, exist_ok=True)

# Initialize an empty list to store form data
form_data_list = []

#esto lo pudiera hacer directamente en el DB con un query!!!
def find_job_by_id(jobs_list, job_id):
  return next((job for job in jobs_list if job['id'] == job_id), None)

@app.route("/")
def helloWorld():
  jobs_list = load_jobs_from_db()
  return render_template("home.html", jobs=jobs_list, companyName="DigitalBori")


@app.route('/apply_form/<int:job_id>', methods=['GET', 'POST'])
def apply_form(job_id):
  jobs_list = load_jobs_from_db()
  job_info = find_job_by_id(jobs_list, job_id)
  if job_info:
    return render_template('apply_form.html', job=job_info, companyName="DigitalBori")
  else:
    # Handle job not found
    return redirect(url_for('helloWorld'))


@app.route('/apply', methods=['POST'])
def submit_application():
  jobs_list = load_jobs_from_db()
  if request.method == 'POST':
    name = request.form['name']
    lastname = request.form['lastname']
    email = request.form['email']
    resume = request.files['resume']
    job_id = int(request.form.get('job_id'))

    # Find the job information based on the job ID
    job_info = find_job_by_id(jobs_list, job_id)

    if job_info:
      # Generate a unique filename for the resume
      resume_filename = f"{name.lower()}_{lastname.lower()}_{resume.filename}"

      # Save the resume file to the "Resumes" folder
      resume_path = os.path.join(RESUMES_FOLDER, resume_filename)
      resume.save(resume_path)

      # Storing application to DB
      add_application_to_db(job_id, name, lastname, email, resume_path, resume_filename)

      # Redirect to confirmation page
      return redirect(
          url_for('confirmation', message='Form submitted successfully!'))

  # If the form submission fails or it's not a POST request, stay on the current page
  return render_template('apply_form.html')


@app.route("/confirmation")
def confirmation():
  return render_template("confirmation.html")


@app.route("/form_data")
def display_form_data():
  return jsonify(form_data_list)

if __name__ == "__main__":
  print("Here")
  app.run(host="0.0.0.0", debug=True)
