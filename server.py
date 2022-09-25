from flask import Flask


app = Flask(__name__)

@app.route('/')
def hell():
    title = "Face ID. Администратор"


    return "Привет!!! Администратор"



if __name__ == '__main__':
    app.run(debug=True)