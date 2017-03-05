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
from settings import MYSQL
from utils import send_error, send_success
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


def validate_claim_id(x):
    claim = Claim.query.filter_by(id=x).first()
    if claim:
        return x
    else:
        raise ValueError("Invalid claim id.")


def create_transaction(netid, amount):
    pass


class GigResource(Resource):
    def get(self, gigid=None):
        ''' Endpoint for getting Gig information '''
        # Return single gig
        if gigid:
            try:
                validate_gig_id(gigid)
            except ValueError:
                return send_error('Invalid gid id')
            gig = Gig.query.filter_by(id=gigid).first()
            return jsonify(gig.to_dict())
        # Return all gigs
        else:
            return jsonify([g.to_dict() for g in Gig.query.all()])

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

    def put(self, gigid):
        ''' Endpoint for activating/deactivating a gig '''
        parser = reqparse.RequestParser()
        parser.add_argument('active', location='json', type=bool,
                            required=True)
        args = parser.parse_args()

        try:
            validate_gig_id(gigid)
        except ValueError:
            return send_error('Invalid gid id')

        gig = Gig.query.filter_by(id=gigid).first()
        gig.active = args.active

        db.session.add(gig)
        db.session.commit()

        active_str = 'active' if args.active else 'closed'
        return send_success('Set gig {} to be {}'.format(gigid, active_str))

    def delete(self, gigid):
        ''' Endpoint for deleting a Gig '''
        try:
            validate_gig_id(gigid)
        except ValueError:
            return send_error('Invalid gid id')

        gig = Gig.query.filter_by(id=gigid).first()
        db.session.delete(gig)
        db.session.commit()
        return send_success('Deleted gig {}'.format(gigid))


class ClaimResource(Resource):
    def get(self, claimid=None):
        ''' Endpoint for getting Claim information '''
        parser = reqparse.RequestParser()
        parser.add_argument('gig_id', location='args')
        args = parser.parse_args()

        claims = Claim.query

        if args.gig_id:
            claims = claims.filter_by(gig_id=args.gig_id)
        return jsonify([c.to_dict() for c in claims.all()])

    def post(self, claimid=None):
        ''' Endpoint for creating a Claim '''
        parser = reqparse.RequestParser()
        parser.add_argument('claimant', location='json', required=True)
        parser.add_argument('gig_id', location='json', required=True,
                            type=validate_gig_id)
        args = parser.parse_args()

        try:
            validate_gig_id(args.gig_id)
        except ValueError:
            return send_error('Invalid gid id')
        gig = Gig.filter_by(gig_id=args.gig_id).first()
        if not gig.active:
            return send_error("Cannot claim an inactive gig")

        claim = Claim(claimant=args.claimant,
                      gig_id=args.gig_id)
        db.session.add(claim)
        db.session.commit()

        return jsonify(claim.to_dict())

    def put(self, claimid):
        ''' Endpoint for accepting a Claim '''
        try:
            validate_claim_id(claimid)
        except ValueError:
            return send_error("Invalid claim id")

        claim = Claim.query.filter_by(id=claimid).first()

        # Don't allow double-fulfills
        if claim.fulfilled:
            return send_error("Claim already fulfilled")

        gig = claim.gig

        # Take credits from creator
        if not gig.admin_task:
            create_transaction(gig.issuer, -1 * gig.credits)
        # Give credits to claimant
        create_transaction(claim.claimant, gig.credits)

        # Mark claim as fulfilled
        claim.fulfilled = True
        db.session.add(claim)
        db.session.commit()

        return send_success("Fulfilled claim {}".format(claimid))

    def delete(self, claimid):
        try:
            validate_claim_id(claimid)
        except ValueError:
            return send_error("Invalid claim id")

        claim = Claim.query.filter_by(id=claimid).first()
        db.session.delete(claim)
        db.session.commit()
        return send_success('Deleted claim {}'.format(claimid))

api = Api(app)
api.add_resource(GigResource, '/gigs', '/gigs/<gigid>')
api.add_resource(ClaimResource, '/gigs/claims', '/gigs/claims/<claimid>')
db.init_app(app)
db.create_all(app=app)

if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    app.run(port=PORT, debug=DEBUG)
