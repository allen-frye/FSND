import os
from os import environ
from urllib import response
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Person, Movies
import json
from datetime import datetime
from flask_cors import CORS
from auth.auth import AuthError, requires_auth

AUTH0_DOMAIN = environ.get('AUTH0_DOMAIN', 'dev-ys2gjmv8t2h7h16t.us.auth0.com')
API_AUDIENCE = environ.get('API_AUDIENCE', 'https://allen-frye-capstone-app-eb15bb134472.herokuapp.com/')
AUTH0_CLIENT_ID = environ.get('AUTH0_CLIENT_ID','59HaFlZDHo6UGEuWrV8KzHKTwzpR6RE6')
AUTH0_CALLBACK_URL = environ.get('AUTH0_CALLBACK_URL', 'https://allen-frye-capstone-app-eb15bb134472.herokuapp.com/response-url')

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    # Add CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
        "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': 
            greeting = greeting + "!!!!! You are doing great in this Udacity project."
        
        return jsonify({
            'greeting': greeting,
            'success': True
        })

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"
    
    @app.route('/response-url')
    def api_response():
        return "api response to get token in URI"

    # Generate token  - (https://knowledge.udacity.com/questions/289182)
   
    @app.route("/authorization/url", methods=["GET"])
    def generate_auth_url():
        url = f'https://{AUTH0_DOMAIN}/authorize' \
            f'?audience={API_AUDIENCE}' \
            f'&response_type=token&client_id=' \
            f'{AUTH0_CLIENT_ID}&redirect_uri=' \
            f'{AUTH0_CALLBACK_URL}'
        return jsonify({
            'url': url
            })

    # Adding Get Actors
    @app.route('/actors', methods=['GET'])
    @requires_auth('view:actors')
    def get_all_actors(token):
        actors = Person.query.all()
        actors_formatted = {actor.id: actor.name for actor in actors}
        
    
        if len(actors_formatted) == 0:
            abort(404)

        return jsonify(
            {
            "success": True,
            "actors_formatted": actors_formatted,

            }
        )
    # Adding Post Actors
    @app.route('/actors', methods=['POST'])
    @requires_auth('create:actors')
    def create_actor(token):
        # print('hello')
        body = request.get_json()
        
        new_name = body.get("name", None)
        new_catchphrase = body.get("catchphrase", None)
        new_age = body.get("age", None)
        new_gender = body.get("gender", None)
        
        if (new_name):
            try:
                actor = Person(name=new_name, catchphrase=new_catchphrase, age=new_age, gender=new_gender)
                # print(actor)
                actor.insert()
                
                return jsonify(
                    {
                        "success": True,
                        "actors": actor.format()
                    }
                    ), 200
            except: 
                abort(422)
        else:
            return jsonify({
                'success': False,
                'actor': []
                }), 404


    # Adding Patch Actors
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actors')
    def update_actor(payload, actor_id):
        body = request.get_json()
        actor = Person.query.filter_by(id=actor_id).one_or_none()

        if (actor is None):
            return jsonify({
                'success': False,
                'actor': []
                }), 404

        new_name = body.get('name')
        new_catchphrase = body.get('catchphrase')
        new_age = body.get('age')
        new_gender = body.get('gender')
        new_movies = body.get('movies')
        new_release_date = body.get('release_date')
        
        if (new_name):
            actor.name = new_name

        if (new_catchphrase):
            actor.catchphrase = new_catchphrase

        if (new_age):
            actor.age = new_age

        if (new_gender):
            actor.gender = new_gender

        if (new_movies):
           
            new_person = actor
            new_release_date_obj = datetime.strptime(new_release_date, '%m/%d/%Y').date()
            new_movie = Movies(title = new_movies, release_date = new_release_date_obj)
            new_person.movies.append(new_movie)
       
        actor.update()
        
         
        return jsonify(
            {
                'success': True,
                'Person Updated': actor.name
            }
        )

    # Delete Actors
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
    
        actor = Person.query.filter_by(id = actor_id).one_or_none()

        if (actor is None):
            return jsonify({
                'success': False,
                'actor': []
                }
            ), 404 

        actor.delete()
        return jsonify(
            {
                "success": True,
                "deleted": actor_id
            }
        )


    # Adding Get Movies
    @app.route('/movies', methods=['GET'])
    @requires_auth('view:movies')
    def get_all_movies(token):
        movies = Movies.query.all()
        movies_formatted = {movie.id: movie.title for movie in movies}
        
    
        if len(movies_formatted) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "movies_formatted": movies_formatted,

            }
        )
    
     # Adding Post Movies
    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movies')
    def create_movie(token):
        # print('hello')
        body = request.get_json()
        
        new_title = body.get("title", None)
        new_release_date = body.get("release_date", None)
        new_release_date_obj = datetime.strptime(new_release_date, '%m/%d/%Y').date()
        
        if (new_title):

            try:

                movie = Movies(title=new_title, release_date=new_release_date_obj)
                
                movie.insert()
                
                return jsonify(
                    {
                        "success": True,
                        "movie": movie.format()
                    }
                    ), 200
            except:
                abort(422)    
        else: 
            return jsonify(
                    {
                        "success": False,
                        "movie": []
                    }
                    ), 404


    # Adding Patch Movies
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:movies')
    def update_movie(payload, movie_id):
        body = request.get_json()
        movie = Movies.query.filter_by(id=movie_id).one_or_none()

        if (movie is None):
            return jsonify({
                'success': False,
                'movie': []
                }), 404

        new_movie = body.get('title')
        new_release_date = body.get('release_date')
        new_release_date_obj = datetime.strptime(new_release_date, '%m/%d/%Y').date()
        
        if (new_movie):
            movie.title = new_movie

        if (new_release_date):
            movie.release_date = new_release_date_obj
       
        movie.update()
        
         
        return jsonify(
            {
                'success': True,
                'Person Updated': movie.title
            }
        )
    
    # Delete Movies
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
    
        movie = Movies.query.filter_by(id = movie_id).one_or_none()

        if (movie is None):
            return jsonify({
                'success': False,
                'movie': []
                }
            ), 404 

        movie.delete()
        return jsonify(
            {
                "success": True,
                "deleted": movie_id
            }
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
            }), 422
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": 'Unathorized'
            }), 401


    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": 'Internal Server Error'
            }), 500


    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": 'Method Not Allowed'
            }), 405 

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "success":False,
            "error": 404,
            "message": "resource not found"
            }), 404

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
            }), error.status_code


    return app

app = create_app()

if __name__ == '__main__':
    # Added Debug
    app.debug = True
    app.run()
