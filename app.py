# -*- coding: utf-8 -*-
'''
Copyright © 2017, ACM@UIUC
This file is part of the Groot Project.
The Groot Project is open source software, released under the University of
Illinois/NCSA Open Source License.  You should have received a copy of
this license in a file with the distribution.
'''
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
import os
from models import db, Gig, Claim
from settings import MYSQL, GROOT_ACCESS_TOKEN, GROOT_SERVICES_URL
import logging
logger = logging.getLogger('groot_meme_service')

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    MYSQL['user'],
    MYSQL['password'],
    MYSQL['host'],
    MYSQL['dbname']
)
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=UTF-8'

PORT = 8964
DEBUG = os.environ.get('GIG_DEBUG', False)


def validate_gig_credits(x):
    x = float(x)
    if x < 0:
        raise ValueError("Credits must be positive")
    return x


def validate_gig_id(x):
    gig = Gig.query.filter_by(id=x).first()
    if gig:
        return x
    else:
        raise ValueError("Invalid gig id.")


class GigResource(Resource):
    def get(self, gigid=None):
        ''' Endpoint for getting Gig information '''
        pass

    def post(self, gigid=None):
        ''' Endpoint for creating a Gig '''
        parser = reqparse.RequestParser()
        parser.add_argument('issuer', location='json', required=True)
        parser.add_argument('description', location='json', default="")
        parser.add_argument('credits', location='json', required=True,
                            type=validate_gig_credits)
        parser.add_argument('admin_task', location='json', type=bool,
                            default=False)

        args = parser.parse_args()
        gig = Gig(issuer=args.issuer,
                  description=args.description,
                  credits=args.credits,
                  admin_task=args.admin_task)
        db.session.add(gig)
        db.session.commit()
        return jsonify(gig.to_dict())

    def delete(self, gigid):
        ''' Endpoint for deleting a Gig '''
        pass


class ClaimResource(Resource):
    def get(self, claimid=None):
        ''' Endpoint for getting Claim information '''
        parser = reqparse.RequestParser()
        parser.add_argument('claimant', location='json', required=True)
        parser.add_argument('gig_id', location='json', required=True,
                            type=validate_gig_id)
        args = parser.parse_args()

        claim = Claim(claimant=args.claimant,
                      gig_id=args.gig_id)
        db.session.add(claim)
        db.session.commit()

        return jsonify(claim.to_dict())

    def post(self, claimid=None):
        ''' Endpoint for creating a Claim '''
        pass

    def put(self, claimid):
        ''' Endpoint for deleting accepting/rejecting a Claim '''
        pass

api = Api(app)
api.add_resource(GigResource, '/gigs', '/gigs/<gigid>')
api.add_resource(ClaimResource, '/gigs/claims', '/gigs/claims/<claimid>')
db.init_app(app)
db.create_all(app=app)

if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    app.run(port=PORT, debug=DEBUG)
