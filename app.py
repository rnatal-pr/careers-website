from flask import Flask, render_template, jsonify

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
  return render_template("home.html", jobs=JOBS)


@app.route("/api/jobs")
def list_jobs():
  return jsonify(JOBS)


if __name__ == "__main__":
  print("Here")
  app.run(host="0.0.0.0", debug=True)
