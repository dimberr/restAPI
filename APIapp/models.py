#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Dealer and Car models"""

from flask_rest_jsonapi import ResourceDetail, ResourceList, ResourceRelationship
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound
from marshmallow_jsonapi.flask import Schema, Relationship
from marshmallow_jsonapi import fields
from APIapp.extensions import db


class Dealer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    address = db.Column(db.String(80))
    working_hours = db.Column(db.String(80))
    cars = db.relationship('Car', backref=db.backref('cars'))


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String())
    model = db.Column(db.String())
    color = db.Column(db.String())
    year = db.Column(db.Integer())
    price = db.Column(db.Integer())
    dealer_id = db.Column(db.Integer, db.ForeignKey('dealer.id'))
    dealer = db.relationship('Dealer', backref=db.backref('dealers'))


# Create schema
class DealerSchema(Schema):
    class Meta:
        type_ = 'dealer'
        self_view = 'dealer_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'dealer_list'

    id = fields.Integer(as_string=True)
    name = fields.Str(load_only=True)
    address = fields.Str()
    working_hours = fields.Str()
    cars = Relationship(self_view='dealer_cars',
                        self_view_kwargs={'id': '<id>'},
                        related_view='car_list',
                        related_view_kwargs={'id': '<id>'},
                        many=True,
                        schema='CarSchema',
                        type_='car')


# Create schema
class CarSchema(Schema):
    class Meta:
        type_ = 'car'
        self_view = 'car_detail'
        self_view_kwargs = {'id': '<id>'}

    id = fields.Integer(as_string=True)
    brand = fields.Str()
    model = fields.Str()
    color = fields.Str()
    year = fields.Str()
    price = fields.Int()
    seller = Relationship(attribute='dealer',
                          self_view='car_dealer',
                          self_view_kwargs={'id': '<id>'},
                          related_view='dealer_detail',
                          related_view_kwargs={'car_id': '<id>'},
                          schema='DealerSchema',
                          type_='dealer')


# Create resource managers
class DealerList(ResourceList):
    schema = DealerSchema
    data_layer = {'session': db.session,
                  'model': Dealer}


class DealerDetail(ResourceDetail):
    def before_get_object(self, view_kwargs):
        if view_kwargs.get('car_id') is not None:
            try:
                car = self.session.query(Car).filter_by(
                    id=view_kwargs['car_id']).one()
            except NoResultFound:
                raise ObjectNotFound({'parameter': 'car_id'},
                                     "Car: {} not found".format(view_kwargs['car_id']))
            else:
                if car.dealer is not None:
                    view_kwargs['id'] = car.dealer.id
                else:
                    view_kwargs['id'] = None

    schema = DealerSchema
    data_layer = {'session': db.session,
                  'model': Dealer,
                  'methods': {'before_get_object': before_get_object}}


class DealerRelationship(ResourceRelationship):
    schema = DealerSchema
    data_layer = {'session': db.session,
                  'model': Dealer}

# Create resource managers
class CarList(ResourceList):
    def query(self, view_kwargs):
        query_ = self.session.query(Car)
        if view_kwargs.get('id') is not None:
            try:
                self.session.query(Dealer).filter_by(
                    id=view_kwargs['id']).one()
            except NoResultFound:
                raise ObjectNotFound(
                    {'parameter': 'id'}, "Dealer: {} not found".format(view_kwargs['id']))
            else:
                query_ = query_.join(Dealer).filter(
                    Dealer.id == view_kwargs['id'])
        return query_

    def before_create_object(self, data, view_kwargs):
        if view_kwargs.get('id') is not None:
            dealer = self.session.query(Dealer).filter_by(
                id=view_kwargs['id']).one()
            data['dealer_id'] = dealer.id

    schema = CarSchema
    data_layer = {'session': db.session,
                  'model': Car,
                  'methods': {'query': query,
                              'before_create_object': before_create_object}}


class CarDetail(ResourceDetail):
    schema = CarSchema
    data_layer = {'session': db.session,
                  'model': Car}


class CarRelationship(ResourceRelationship):
    schema = CarSchema
    data_layer = {'session': db.session,
                  'model': Car}
