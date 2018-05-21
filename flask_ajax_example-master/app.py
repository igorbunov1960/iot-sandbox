from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/_hit_button')
def hit_button():
    print('hit button called')
    return jsonify(text='success!')

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int('80'),
        debug=True
    )
