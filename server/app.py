#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User, UserSchema

user_schema = UserSchema()

class Signup(Resource):

    def post(self):
        
        username = request.json.get('username')
        password = request.json.get('password')
        
        user = User(username=username)
        user.password_hash = password
        
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = user.id
        
        return user_schema.dump(user), 201

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(ClearSession, '/clear', endpoint='clear')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
