from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from typing import List

app = Flask(__name__)

if app.config["ENV"] == "test":  # Evaluates to true if FLASK_ENV=test
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root@database:3306/productiondb'

db = SQLAlchemy(app)
api = Api(app)


class User(db.Model):
    """ A SQLAlchemy Model used to store information about a user. This only
    needs to have a collection of class variables that are of type db.Column.
    # TODO: Add a column so that this can HAVE several GameScores
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    game_scores = db.relationship('GameScore', backref='user', lazy=True)


class GameScore(db.Model):
    """ A SQLAlchemy Model used to store information a score.
    # TODO: Add a column so that this can also refer to a specific user
    """
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(128), nullable=False)
    value = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class UserListResource(Resource):
    """ A Resource is a collection of routes (think URLs) that map to these functions.
    For a REST API, we have GET, PUT, POST, PATCH, DELETE, etc. Here we just define
    functions that map to the REST API verbs, later we map this to a specific URL
    with api.add_resource
    """

    def get(self) -> List[dict]:
        """Responds to http://[domain or IP]:[port (default 5000)]/users

        Returns:
            List of dictionaries describing all users in the database. We should only include some information if
            passwords or other personal information is involved.
        """
        return [{"username": user.username, "id": user.id} for user in User.query.all()]

    def post(self) -> dict:
        """Responds to http://[domain or IP]:[port (default 5000)]/users.

        Adds a new user to the database.

        Returns:
            Dictionary describing user that was just created.
        """
        new_user = User(username=request.json['username'])
        db.session.add(new_user)
        db.session.commit()
        return {"username": request.json["username"]}

    def delete(self):
        """Responds to http://[domain or IP]:[port (default 5000)]/users.

        deletes all users in the database

        Returns:
            Dictionary describing user that was just created.
        """
        User.__table__.drop(db.session)
        User.__table__.create(db.session)


class UserResource(Resource):
    """ UserResource is slightly different from UserListResource as these functions will only respond
    to Responds to http://[domain or IP]:[port (default 5000)]/users/<user_id> so these are always
    executed in the context of a specific user.

    """

    def get(self, user_id):
        """Responds to http://[domain or IP]:[port (default 5000)]/users/<user_id>

        Returns:
            Dictionary describing user by user_id
        """
        user = User.query.get_or_404(user_id)
        return {"id": user.id, "username": user.username}

    def patch(self, user_id):
        """Responds to http://[domain or IP]:[port (default 5000)]/users/<user_id>

        This is used to update an existing user.

        Returns:
           Dictionary describing user that was changed.
        """
        user = User.query.get_or_404(user_id)

        if 'username' in request.json:
            user.username = request.json['username']

        db.session.commit()
        return {"id": user.id, "username": user.username}

    def delete(self, user_id):
        """Responds to http://[domain or IP]:[port (default 5000)]/users/<user_id>

        This is used to delete an existing user

        Returns:
           Dictionary describing user that was changed.
        """
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204


class UserListResource(Resource):
    """ A Resource is a collection of routes (think URLs) that map to these functions.
    For a REST API, we have GET, PUT, POST, PATCH, DELETE, etc. Here we just define
    functions that map to the REST API verbs, later we map this to a specific URL
    with api.add_resource
    """

    def get(self) -> List[dict]:
        """Responds to http://[domain or IP]:[port (default 5000)]/users

        Returns:
            List of dictionaries describing all users in the database. We should only include some information if
            passwords or other personal information is involved.
        """
        return [{"username": user.username, "id": user.id} for user in User.query.all()]

    def post(self) -> dict:
        """Responds to http://[domain or IP]:[port (default 5000)]/users.

        Adds a new user to the database.

        Returns:
            Dictionary describing user that was just created.
        """
        new_user = User(username=request.json['username'])
        db.session.add(new_user)
        db.session.commit()
        return {"username": request.json["username"]}


class UserGameScoreResource(Resource):
    """Responds to http://[domain or IP]:[port (default 5000)]/api/v1/scores/<user_id> so these are always
    executed in the context of a specific user.

    """

    def get(self, user_id):
        """Responds to http://[domain or IP]:[port (default 5000)]/api/v1/scores/<user_id>

        # TODO: return game_name and value for all scores

        Returns:
            Dictionary describing user by user_id
        """
        user = User.query.get_or_404(user_id)
        return [{"game_name": game_score.game_name, "value": game_score.value} for game_score in user.game_scores]

    def post(self, user_id) -> dict:
        """Responds to http://[domain or IP]:[port (default 5000)]/api/v1/scores/<user_id>.

        # TODO: Create new GameScore and return game_name, value, and user_id

        Returns:
            Dictionary describing user score that was just created
        """
        new_score = GameScore(user_id=user_id, game_name=request.json['game_name'],
                              value=request.json['value'])
        db.session.add(new_score)
        db.session.commit()
        return {
            "game_name": request.json["game_name"],
            "value": request.json["value"],
            "user_id": user_id
        }


class ResetResource(Resource):
    """Responds to http://[domain or IP]:[port (default 5000)]/api/v1/reset

    Notes:
        This is just a convenience endpoint to reset the database.
    """

    def post(self):
        db.drop_all()
        db.create_all()


api.add_resource(UserListResource, '/api/v1/users')
api.add_resource(UserResource, '/api/v1/users/<int:user_id>')
api.add_resource(ResetResource, '/api/v1/reset')

# TODO: Link the UserGameScoreResource to the appropriate URL endpoint
api.add_resource(UserGameScoreResource, '/api/v1/scores/<user_id>')


def create_app():
    """ This is used as a factory function for creating the entire application instance
    when the application is first run. Best practices for FLASK is to allow creating an 
    application instance ONLY using this function for very good reasons, but this
    is good enough to use for now.
    """
    try:
        db.create_all()
    except Exception as e:
        print("Not populating tables -- they already exist.")
    return app


if __name__ == "__main__":
    app.run()
