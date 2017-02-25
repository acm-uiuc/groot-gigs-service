# -*- coding: utf-8 -*-
'''
Copyright © 2017, ACM@UIUC
This file is part of the Groot Project.
The Groot Project is open source software, released under the University of
Illinois/NCSA Open Source License.  You should have received a copy of
this license in a file with the distribution.
'''
from flask import Flask
from flask_restful import Resource, Api, reqparse
import os
from models import db, Gig
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


class GigResource(Resource):
    def get(self, gigid=None):
        ''' Endpoint for getting Gig information '''
        pass

    def post(self, gigid=None):
        ''' Endpoint for creating a Gig '''
        pass

    def delete(self, gigid):
        ''' Endpoint for deleting a Gig '''
        pass


class ClaimResource(Resource):
    def get(self, claimid=None):
        ''' Endpoint for getting Claim information '''
        pass

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
