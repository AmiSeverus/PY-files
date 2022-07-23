import atexit
from unicodedata import name
from flask import Flask, jsonify, request
from flask.views import MethodView
import requests
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/flask')
Base = declarative_base()
Session = sessionmaker(bind=engine)
atexit.register(lambda: engine.dispose())

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

class Adv(Base):
    __tablename__='advs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))

Base.metadata.create_all(engine)

app = Flask('api')

class AdvView(MethodView):
    def get(self):
        pass

    def post(self):
        json = request.json 

class UserView(MethodView):
    def get(self):
        pass

    def post(self):
        json_data = request.json
        return jsonify(json_data)
        with Session() as session:
            # new_user = User(name=json_data['name'])
            # session.add(new_user)
            # session.commit()
            return jsonify({
                'id': json_data
            })

@app.route('/', methods=['GET'])
def get_advs():
    return jsonify({'status':'Ok'})

@app.route('/adv/', methods=['POST'])
def add_adv():
    json_data = request.json
    return jsonify(json_data)

app.add_url_rule('/users/', view_func=UserView.as_view('create_user'), methods=['POST'])

app.run(
    host='0.0.0.0',
    port=5050
)