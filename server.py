from flask import Flask, render_template, request
from appraisal import get_effect_averages, get_price

app = Flask(__name__)
app.debug = True


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        return str(get_price(request.form["hatname"], request.form["hateffect"])) + " keys"


@app.route('/effect_averages')
def effect_averages():
    return str(app.config["effect_averages"])


if __name__ == '__main__':
    print('downloading')
    app.config["effect_averages"] = get_effect_averages()
    app.run()
