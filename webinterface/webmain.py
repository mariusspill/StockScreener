from flask import Flask, render_template, request, jsonify
import webinterface.data_transfer as dt
import analysis.analysis_screening as ascreen
import helpers.tickers as tickers

app = Flask(__name__)
tckrs = tickers.getTickers("./helpers/list.txt")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/screen', methods=['POST'])
def screen():
    data = request.get_json()
    param = data.get('pe')
    dt.shared.set_pe(int(param))
    dt.shared.set_list(ascreen.Screening_as_dict(ascreen.list_of_stocks(tckrs), param))
    return jsonify(dt.shared.get_list())

def runFlask():
    app.run(debug=True, use_reloader=False)


if __name__ == "__main__":
    app.run(debug=True)