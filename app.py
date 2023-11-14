from flask import Flask, jsonify, render_template, request, redirect, url_for
import os

app = Flask(__name__)

JOBS = [{
    'id': 1,
    'title': 'Data Analyst',
    'location': 'Bayamon, PR',
    'salary': '45k-65k'
}, {
    'id': 2,
    'title': 'Data Scientist',
    'location': 'Guaynabo, PR',
    'salary': '55k-75k'
}, {
    'id': 3,
    'title': 'Data Engineer',
    'location': 'San Juan, PR',
    'salary': '55k-755k'
}]

# Set the path for the "Resumes" folder
RESUMES_FOLDER = os.path.join(os.getcwd(), 'Resumes')

# Create the "Resumes" folder if it doesn't exist
os.makedirs(RESUMES_FOLDER, exist_ok=True)

# Initialize an empty list to store form data
form_data_list = []


@app.route("/")
def helloWorld():
  return render_template("home.html", jobs=JOBS, companyName="DigitalBori")


@app.route('/apply_form/<int:job_id>', methods=['GET', 'POST'])
def apply_form(job_id):
  job_info = next((job for job in JOBS if job['id'] == job_id), None)

  if job_info:
    return render_template('apply_form.html', job=job_info)
  else:
    # Handle job not found
    return redirect(url_for('helloWorld'))


@app.route('/apply', methods=['POST'])
def submit_application():
  if request.method == 'POST':
    name = request.form['name']
    lastname = request.form['lastname']
    email = request.form['email']
    resume = request.files['resume']
    job_id = int(request.form.get('job_id'))

    # Find the job information based on the job ID
    job_info = next((job for job in JOBS if job['id'] == job_id), None)

    if job_info:
      # Generate a unique filename for the resume
      resume_filename = f"{name.lower()}_{lastname.lower()}_{resume.filename}"

      # Save the resume file to the "Resumes" folder
      resume.save(os.path.join(RESUMES_FOLDER, resume_filename))

      # Store the job information, filename, and other form data in the list
      form_data = {
          'job_id': job_info['id'],
          'job_title': job_info['title'],
          'job_location': job_info['location'],
          'job_salary': job_info['salary'],
          'name': name,
          'lastname': lastname,
          'email': email,
          'resume_filename': resume_filename
      }
      form_data_list.append(form_data)

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


@app.route("/api/jobs")
def list_jobs():
  return jsonify(JOBS)


if __name__ == "__main__":
  print("Here")
  app.run(host="0.0.0.0", debug=True)
