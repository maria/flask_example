from datetime import datetime
import flask
from flask.ext.sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


@app.route('/')
def home():
    return flask.render_template('message.html',
            messages=Message.query.all())

@app.route('/new', methods=['GET', 'POST'])
def new():
    if flask.request.method == 'POST':

        text = flask.request.form['message']
        message = Message(text=text, time=datetime.utcnow())
        db.session.add(message)
        db.session.commit()
        return flask.redirect(flask.url_for('home'))

    return flask.render_template('new.html')

@app.template_filter()
def tolower(value):
    return value.lower()

class Message(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        text = db.Column(db.String)
        time = db.Column(db.DateTime)

if __name__ == '__main__':
    db.create_all()
    app.run()
