from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    messages = Message.query.all()
    if request.method == 'GET':
        messages_dict = [message.to_dict() for message in messages]

        return make_response(
            messages_dict,
            200
        )
    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body = data['body'],
            username = data['username'],
        )
        db.session.add(new_message)
        db.session.commit()

        new_message_dict = new_message.to_dict()

        return make_response(
            new_message_dict,
            201
        )


@app.route('/messages/<int:id>', methods = ['PATCH', 'DELETE'])
def messages_by_id(id):
    messages_by_id = Message.query.filter(Message.id == id).first()
    if request.method == 'PATCH':
        data = request.get_json()
        for attr in data:
            setattr(messages_by_id, attr, data[attr])
            db.session.add(messages_by_id)
            db.session.commit()

            messages_by_id_dict = messages_by_id.to_dict()
            return make_response(
                messages_by_id_dict,
                200
            )

    elif request.method == 'DELETE':
        db.session.delete(messages_by_id)
        db.session.commit()
        return make_response({
            'deleted': True},
            200
            )

if __name__ == '__main__':
    app.run(port=5555)
