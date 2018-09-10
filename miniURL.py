from flask import Flask, request, render_template, make_response

app = Flask(__name__)

@app.route("/")
@app.route("/shortenURL", methods=["POST"])
def shortenURL():
    longURL = None
    if request.method == 'POST':
        longURL = request.form['longURL']
        print(longURL)
    response = make_response(render_template('index.html'))
    if longURL:
        response.set_cookie('longURL', longURL)
    return response

if __name__ == "__main__":
    app.run()
