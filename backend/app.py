from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.

    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)

@app.route("/shows", methods=['GET'])
def get_all_shows():
    print( db.get('shows') )
    if request.args.get('minEpisodes') != None:
        minEpisodes = int(request.args.get('minEpisodes'))
        shows_to_return = []

        for show in db.get('shows'):
            if int(show["episodes_seen"]) >= minEpisodes:
                shows_to_return.append(show)


        if len(shows_to_return) == 0:
            return create_response(status=404, message="No show with the given minEpisodes exist")
        return create_response({"shows": shows_to_return})

    else:
        return create_response({"shows": db.get('shows')})


@app.route("/shows/<id>", methods=['DELETE'])
def delete_show(id):
    if db.getById('shows', int(id)) is None:
        return create_response(status=404, message="No show with this id exists")
    db.deleteById('shows', int(id))
    return create_response(message="Show deleted")


# TODO: Implement the rest of the API here!

'''
Part 2 of the assignment
param : id of the show
retrieves a single show that has the given id
'''
@app.route("/shows/<id>", methods=['GET'])
def get_show(id):
    if db.getById('shows', int(id)) is None:
        return create_response(status=404, message="No show with this id exists")
    return create_response({"show": db.getById('shows', int(id))})

'''
Part 4 of the assignment
param : takes the name and episodes_seen parameters in the body
        Creates a new show in the database if the correct parameters are passed or else returns a 422 error
'''
@app.route("/shows", methods=['POST'])
def add_show():


    body = request.get_json()
    if "name" in body and "episodes_seen" in body:
        newShow = { "name": body["name"], "episodes_seen" : int(body["episodes_seen"]) }
        db.create('shows', newShow)
        for show in db.get('shows'):
            if str(show["name"]) == str(newShow["name"]):
                return create_response({"shows": show},201)

    else:
        if "name" not in body and "episodes_seen" not in body:
            return create_response(status=422, message= "name and the episodes_seen parameters not passed in body")
        elif "name" not in body:
            return create_response(status=422, message= "name parameter not passed in body")
        elif "episodes_seen" not in body:
            return create_response(status=422, message= "episodes_seen parameter not passed in body")



'''
Part 5 of the assignment
param : takes the id of the show to update
        Updates the show in the database with the new values.
'''

@app.route("/shows/<id>", methods=['PUT'])
def update_show(id):
    if db.getById('shows', int(id)) is None:
        return create_response(status=404, message="No show with this id exists")

    body = request.get_json()
    if "name" in body or "episodes_seen" in body:
        existing_show = db.updateById('shows', int(id), body)
    else:
        return create_response(status=422, message="Nothing to update")
    return create_response({"show": db.getById('shows', int(id))})








"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(port=8080, debug=True)
