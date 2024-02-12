import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this function will add one
'''
db_drop_and_create_all()

@app.route('/')
def handler():
    return jsonify({
        "success": True
    })

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
#source: https://github.com/erinlouise11/Coffee-Shop/blob/master/backend/src/api.py#L21
@app.route('/drinks', methods=['GET'])
def get_drinks():
    # getting all the drinks from the database
    drinks = Drink.query.all()
    short_drinks = []

    # getting the short representation for each drink and adding it to a list of short_drinks
    for drink in drinks:
        short_drinks.append(drink.short())

    # return the json object
    if len(short_drinks) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'drinks': short_drinks
    }), 200

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(token):
# def get_drinks_detail():
    drinks = Drink.query.all()
    long_drinks = []
    # print(drinks)
    for drink in drinks:
        long_drinks.append(drink.long())
    print("Get:")
    print(long_drinks)    
    if len(long_drinks) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'drinks': long_drinks
    }), 200




'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods=['POST'])
# @requires_auth('post:drinks')
# def post_drinks(token):
def post_drinks():
    body = request.get_json()

    # if not ('title' in body and 'recipe' in body):
    #     abort(422)

    new_title = body["title"]
    # new_recipe = body.get("recipe", None)
    new_recipe = json.dumps(body["recipe"])
    # print(new_recipe + new_title)
    try:
      drink = Drink(title=new_title, recipe=new_recipe)
      drink.insert()
      print("Post")
      print(drink.long())
      return jsonify(
        {
          "success": True,
          "drinks": [drink.long()]
          }
      ), 200

    except:
        abort(422)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
# add auth
def update_drink(drink_id):
    body = request.get_json()
    drink = Drink.query.filter_by(id=drink_id).one_or_none()

    if (drink is None):
        return jsonify({
            'success': False,
            'drinks': []
            }), 404

    new_title = body.get('title')
    print(body.get('title'), end="\n")
    new_recipe = body.get('recipe')
   
    if (new_title):
        drink.title = new_title

    if (new_recipe):
        drink.recipe = json.dumps(body['recipe'])

    drink.update()
    print("Patch")
    print(drink.long())   
    return jsonify({
        'success': True,
        'drinks': [drink.long()]

        })



'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
def delete_drink(drink_id):
    drink_test = Drink.query.all()
    print(drink_test)
    drink = Drink.query.filter_by(id = drink_id).one_or_none()

    if (drink is None):
        return jsonify({
            'success': False,
            'drinks': []
        }), 404 

    drink.delete()
    return jsonify(
        {
        "success": True,
        "delete": drink_id
        }
    )




# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''

if __name__ == "__main__":
    app.debug = True
    app.run()
