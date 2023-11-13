from flask import Flask, jsonify, render_template, request

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


@app.route("/")
def helloWorld():
  return render_template("home.html", jobs=JOBS, companyName="DigitalBori")


@app.route('/apply', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    name = request.form['name']
    lastname = request.form['lastname']
    email = request.form['email']
    resume = request.files['resume']

    # tengo que guardar la data

    return render_template('index.html',
                           message='Form submitted successfully!')

  return render_template('index.html')


@app.route("/api/jobs")
def list_jobs():
  return jsonify(JOBS)


if __name__ == "__main__":
  print("Here")
  app.run(host="0.0.0.0", debug=True)
