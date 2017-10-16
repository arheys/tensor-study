from flask import Flask, request
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)


db.create_all()

api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(Person, methods=['GET', 'POST', 'DELETE', 'PUT'])


@app.route('/hello')
def hell0():
    return "Hello"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        res = request.get_json()
        return res['username']

    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''
if __name__ == "__main__":
    app.run()