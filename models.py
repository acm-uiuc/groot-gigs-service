# -*- coding: utf-8 -*-
'''
Copyright © 2017, ACM@UIUC
This file is part of the Groot Project.
The Groot Project is open source software, released under the University of
Illinois/NCSA Open Source License.  You should have received a copy of
this license in a file with the distribution.
'''

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Gig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issuer = db.Column(db.String(100))
    description = db.Column(db.String(150))
    credits = db.Column(db.Float())
    admin_task = db.Column(db.Boolean, default=False)
    claims = db.relationship('Claim', backref='gig', lazy='dynamic')
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "issuer": self.issuer,
            "description": self.description,
            "credits": self.credits,
            "created_at": self.created_at.isoformat(),
            "active": self.active
        }


class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    claimant = db.Column(db.String(100))
    fulfilled = db.Column(db.Boolean, default=False)
    gig_id = db.Column(db.Integer, db.ForeignKey('gig.id'))
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "claimant": self.claimant,
            "fulfilled": self.fulfilled,
            "gig_id": self.gig_id,
            "created_at": self.created_at.isoformat()
        }
