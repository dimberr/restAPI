#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Small REST API app based on Flask and flask-rest-jsonapi package that supports CRUD operations"""

from flask import Flask
from flask_rest_jsonapi import Api
from APIapp.models import CarDetail, CarList, CarRelationship, DealerDetail, DealerList, DealerRelationship
from APIapp.extensions import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create DB for app
db.app = app
db.init_app(app)
db.create_all()

# Create API for routing
api = Api(app)
api.init_app(app)

api.route(DealerList, 'dealer_list', '/dealers')
api.route(DealerDetail, 'dealer_detail',
          '/dealers/<int:id>', '/cars/<int:car_id>/seller')
api.route(DealerRelationship, 'dealer_cars',
          '/dealers/<int:id>/relationships/cars')
api.route(CarList, 'car_list', '/cars', '/dealers/<int:id>/cars')
api.route(CarDetail, 'car_detail', '/cars/<int:id>')
api.route(CarRelationship, 'car_dealer',
          '/dealers/<int:id>/relationships/seller')
