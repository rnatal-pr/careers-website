from flask import Flask

app = Flask(__name__)


@app.route("/")
def helloWorld():
  return "Hello, Flaski!"


if __name__ == "__main__":
  print("Here")
  app.run(host="0.0.0.0", debug=True)
