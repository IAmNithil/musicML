from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        return 'Return using POST'
    else:
        return 'Return using GET'


if __name__ == '__main__':
    app.run()
