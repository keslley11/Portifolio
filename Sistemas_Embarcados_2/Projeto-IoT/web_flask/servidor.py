from flask import Flask, render_template, Response
import datetime

app = Flask(__name__)

# dados = [
#     {'temp':0,'datetime': datetime.datetime.now()}
# ]

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
