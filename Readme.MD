### Small REST API app based on Flask and flask-rest-jsonapi package that supports CRUD operations



##### Install pip requirements
Acivate your venv, then run:

`$ pip install -r requirements.txt`

##### Running app

`export FLASK_APP=app.py` 
`flask run`

##### Check that app started to run at:
`http://127.0.0.1:5000/`

                    
### API examples
                    


| Url      | Method | Endpoint | Action
| ------ | ----------| -----------| -------|
| /dealers  | GET | dealer_list | Retrieve a collection of dealers |
| /dealers | POST | dealer_list |Create a dealer |
|/dealers/&lt;int:id>| GET | dealer_detail | Retrieve details of a dealer |
|/dealers/&lt;int:id> | PATCH | dealer_detail | Update a dealer |
|/dealers/&lt;int:id> | DELETE | dealer_detail | Delete a dealer |
|/dealers/&lt;int:id>/cars | GET | car_list | Retrieve a collection cars related to a dealer |
|/dealers/&lt;int:id>/cars | POST | car_list | Create a car related to a dealer |
| /dealers/&lt;int:id>/relationship/cars | GET | dealer_cars | Retrieve relationships between a dealer and cars |
| /dealers/&lt;int:id>/relationship/cars | POST | dealer_cars | Create relationships between a dealer and cars |
| /dealers/&lt;int:id>/relationship/cars | PATCH | dealer_cars | Update relationships between a dealer and cars |
| /dealers/&lt;int:id>/relationship/cars | DELETE | dealer_cars | Delete relationships between a dealer and cars |
| /cars | GET | car_list | Retrieve a collection of cars |
| /cars | POST | car_list | Create a car | 
| /cars/&lt;int:id> | GET | car_detail | Retrieve details of a car |
| /cars/&lt;int:id> | PATCH | car_detail | Update a car| 
| /cars/&lt;int:id> | DELETE | car_detail | Delete a car|
| /cars/&lt;int:id>/seller | GET | dealer_detail | Retrieve details of the seller of a car |
| /cars/&lt;int:id>/seller | PATCH | dealer_detail | Update the seller of a car |
| /cars/&lt;int:id>/seller | DELETE | dealer_detail | Delete the seller of a car |
| /cars/&lt;int:id>/relationship/seller | GET | dealer_cars | Retrieve relationships between a dealer and cars |
| /cars/&lt;int:id>/relationship/seller | POST | dealer_cars | Create relationships between a dealer and cars | 
| /cars/&lt;int:id>/relationship/seller | PATCH | dealer_cars | Update relationships between a dealer and cars |
| /cars/&lt;int:id>/relationship/seller | DELETE | dealer_cars | Delete relationships between a dealer and cars |

### Classical CRUD operations

#### Create object
Request:
```json
POST /computers HTTP/1.1
Content-Type: application/vnd.api+json
Accept: application/vnd.api+json
{
    "data": {
        "type": "car",
        "attributes": {
            "brand": "Lada",
            "model": "Kalina",
            "color": "green",
            "year": "1990",
            "price": 2000
        }
    }
}
```
Response:
```json
HTTP/1.1 201 Created
Content-Type: application/vnd.api+json
{
    "data": {
        "type": "car",
        "relationships": {
            "seller": {
                "links": {
                    "self": "/dealers/1/relationships/seller",
                    "related": "/cars/1/seller"
                }
            }
        },
        "attributes": {
            "color": "green",
            "year": "1990",
            "model": "Kalina",
            "brand": "Lada",
            "price": 2000
        },
        "id": "1",
        "links": {
            "self": "/cars/1"
        }
    },
    "links": {
        "self": "/cars/1"
    },
    "jsonapi": {
        "version": "1.0"
    }
}
```
#### List objects
Request:
```json
GET /cars HTTP/1.1
Accept: application/vnd.api+json
```
Response:
```json
HTTP/1.1 200 OK
Content-Type: application/vnd.api+json
{
    "data": [
        {
            "type": "car",
            "relationships": {
                "seller": {
                    "links": {
                        "self": "/dealers/1/relationships/seller",
                        "related": "/cars/1/seller"
                    }
                }
            },
            "attributes": {
                "color": "green",
                "year": "1990",
                "model": "Kalina",
                "brand": "Lada",
                "price": 2000
            },
            "id": "1",
            "links": {
                "self": "/cars/1"
            }
        }
    ],
    "links": {
        "self": "http://localhost:5000/cars"
    },
    "meta": {
        "count": 1
    },
    "jsonapi": {
        "version": "1.0"
    }
}
```
#### Update object
Request:
```json
PATCH /cars/1 HTTP/1.1
Content-Type: application/vnd.api+json
Accept: application/vnd.api+json
{
    "data": {
        "type": "car",
        "id": "1",
        "attributes": {
            "brand": "Lada",
            "model": "Kalina",
            "color": "red",
            "year": "1990",
            "price": 2000
        }
    }
}
```
Response:
```json
HTTP/1.1 200 OK
Content-Type: application/vnd.api+json
{
    "data": {
        "type": "car",
        "attributes": {
            "model": "Kalina",
            "year": "1990",
            "color": "red",
            "price": 2000,
            "brand": "Lada"
        },
        "id": "1",
        "relationships": {
            "seller": {
                "links": {
                    "self": "/dealers/1/relationships/seller",
                    "related": "/cars/1/seller"
                }
            }
        },
        "links": {
            "self": "/cars/1"
        }
    },
    "links": {
        "self": "/cars/1"
    },
    "jsonapi": {
        "version": "1.0"
    }
}
```
#### Create object with related object(s)
```json
POST /dealers?include=cars HTTP/1.1
Content-Type: application/vnd.api+json
Accept: application/vnd.api+json

{
  "data": {
    "type": "dealer",
    "attributes": {
      "name": "LadaDistributions",
      "address": "Saint-Petersburg, Nevsky, 33",
      "working_hours": "08:00-22:00"
    },
    "relationships": {
      "cars": {
        "data": [
          {
            "type": "car",
            "id": "1"
          }
        ]
      }
    }
  }
}
```
Response:
```json
HTTP/1.1 201 Created
Content-Type: application/vnd.api+json
{
    "data": {
        "type": "dealer",
        "id": "1",
        "attributes": {
            "address": "Saint-Petersburg, Nevsky, 33",
            "working_hours": "08:00-22:00"
        },
        "relationships": {
            "cars": {
                "links": {
                    "self": "/dealers/1/relationships/cars",
                    "related": "/dealers/1/cars"
                },
                "data": [
                    {
                        "type": "car",
                        "id": "1"
                    }
                ]
            }
        },
        "links": {
            "self": "/dealers/1"
        }
    },
    "links": {
        "self": "/dealers/1"
    },
    "included": [
        {
            "type": "car",
            "id": "1",
            "attributes": {
                "price": 2000,
                "year": "1990",
                "color": "red",
                "brand": "Lada",
                "model": "Kalina"
            },
            "relationships": {
                "seller": {
                    "links": {
                        "self": "/dealers/1/relationships/seller",
                        "related": "/cars/1/seller"
                    }
                }
            },
            "links": {
                "self": "/cars/1"
            }
        }
    ],
    "jsonapi": {
        "version": "1.0"
    }
}
```
#### Delete relationship
Request:
```json
DELETE /dealers/1/relationships/cars HTTP/1.1
Content-Type: application/vnd.api+json
Accept: application/vnd.api+json

{
  "data": [
    {
      "type": "car",
      "id": "1"
    }
  ]
}
```
Response:
```json
HTTP/1.1 200 OK
Content-Type: application/vnd.api+json
{
    "meta": {
        "message": "Relationship successfully updated"
    },
    "jsonapi": {
        "version": "1.0"
    }
}
```
#### Delete object
Request:
```json
DELETE /cars/1 HTTP/1.1
Accept: application/vnd.api+json

```
Response:
```json
HTTP/1.1 200 OK
Content-Type: application/vnd.api+json
{
    "meta": {
        "message": "Object successfully deleted"
    },
    "jsonapi": {
        "version": "1.0"
    }
}
```