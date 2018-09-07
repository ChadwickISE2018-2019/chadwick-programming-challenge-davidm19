import flask
from flask import Flask, request
from server.dao import Customer, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
app = Flask(__name__)

'''
Setup the /customer route. It accepts, GET, POST, and PUT requests
'''
@app.route('/customer', methods=["GET", "POST", "PUT"])
def customer():
    methods = { "GET": get_customer
              , "POST": add_customer
              , "PUT": update_customer
              }
    if request.method in methods:
        return methods[request.method]()

    return flask.jsonify("Invalid Request"), 400

'''
Get the customers that meet the specified parameters. The result should be a list.
Examples:
  # Returns the customer with the id 1.
  $ curl 'localhost:8888/customer?id=1'

  # Returns all customers
  $ curl 'localhost:8888/customer'

  # Returns all customers with the first_name 'Bill'
  $ curl 'localhost:8888/customer?first_name=Bill'

  # Returns all customers with the last_name 'Johnson'
  $ curl 'localhost:8888/customer?last_name=Johnson'

  # Returns all customers with the first_name 'Bill' and last_name 'Johnson'
  $ curl 'localhost:8888/customer?first_name=Bill&last_name=Johnson'
'''
def get_customer():
    session = Session()
    customer_id = request.args.get('id')
    customer = session.query(Customer).filter(Customer.id == 1).one()
    customer_info = { "first_name" : customer.first_name
                    , "last_name" : customer.last_name
                    , "email" : customer.email
                    , "id" : customer.id
                    }
    return flask.jsonify([customer_info]), 200

'''
Adds a customer to the database. The request expects the
header: "Content-Type: application/json" and json object containing at least 
a first_name and last_name field.

Examples:
# Creates a new Customer Record named John Doe
curl -H "Content-Type: application/json" \
     -X POST -d '{"first_name": "John", "last_name": "Doe"}' \
     'localhost:8888/customer'

# Invalid request (must have a first_name and a last_name)
curl -H "Content-Type: application/json" \
     -X POST -d '{"last_name": "Doe"}' \
     'localhost:8888/customer'

# Creates a new Customer Record named John Doe with the email johndoe@yahoo.com
curl -H "Content-Type: application/json" \
     -X POST -d '{"first_name": "John", "last_name": "Doe", "email": "johndoe@yahoo.com"}' \
     'localhost:8888/customer'

'''
def add_customer():
    post = request.get_json()
    print(post)
    return "TODO: Implement", 200


'''
Updates a customer record with the specified information. 
The request expects the header: "Content-Type: application/json" and
json object containing an id of the customer to update.

If the id does not exist, a 404 error is returned

Examples:
# Updates the row with id 1 to have the name John Doe
curl -H "Content-Type: application/json" \
     -X PUT -d '{"id": 1, "first_name": "John", "last_name": "Doe"}' \
     'localhost:8888/customer'

# Updates the row with id 1 to have the email john@doe.com
curl -H "Content-Type: application/json" \
     -X PUT -d '{"id": 1, "email": "john@doe.com"}' \
     'localhost:8888/customer'
'''
def update_customer():
    post = request.get_json()
    print(post)
    return "TODO: Implement", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
