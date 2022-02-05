from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import random
import os

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
load_dotenv()


class DataMod(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    reason = db.Column(db.String, nullable=False)
    reported_times = db.Column(db.Integer, nullable=False)


db.create_all()

put_args = reqparse.RequestParser()
put_args.add_argument(
    "id", type=int, help="Discord user ID is required. Right click on a user in developer mode to get it.", required=True)
put_args.add_argument(
    "reason", type=str, help="A reason is required. Please provide a detailed description.", required=True)
put_args.add_argument("reported_times", type=int,
                      help="This is the number of times a user has been reported. This API will handel that.")

update_args = reqparse.RequestParser()
update_args.add_argument(
    "id", type=int, help="Discord user ID is required. Right click on a user in developer mode to get it.", required=True)
update_args.add_argument(
    "reason", type=str, help="A reason is required. Please provide a detailed description.", required=True)
update_args.add_argument("reported_times", type=int,
                         help="This is the number of times a user has been reported. This API will handel that.")

resource_fields = {
    'id': fields.Integer,
    'reason': fields.String
}


trusted_ips = [os.getenv("TRUSTED_IP")]


class Main(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        result = DataMod.query.filter_by(id=id).first()
        if not result:
            abort(404, message="This user could not be found in our database. This user has not been reported. (404)")
        return result

    @marshal_with(resource_fields)
    def put(self, id):
        args = put_args.parse_args()
        result = DataMod.query.filter_by(id=id).first()
        if result:
            abort(409, message=f"This user is already in our database. (409)")
        user = DataMod(id=args['id'], reason=args['reason'], reported_times=1)
        db.session.add(user)
        db.session.commit()
        return f"This user has been entered. Log: {user}", 201

    @marshal_with(resource_fields)
    def patch(self, id):
        if request.remote_addr not in trusted_ips:
            abort(403)
        args = update_args.parse_args()
        result = RockMod.query.filter_by(id=id).first()
        if not result:
            abort(404, message="This user does not exist. Could not update. (404)")

        if args['id']:
            result.id = args['id']
        if args['reason']:
            result.reason = args['reason']
        db.session.commit()

        return result


api.add_resource(Main, "/search/<int:id>")
if __name__ == "__main__":
    app.run(debug=True)
