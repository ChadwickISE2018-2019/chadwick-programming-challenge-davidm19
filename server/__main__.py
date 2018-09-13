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
    customer_firstname = request.args.get('first_name')
    customer_lastname = request.args.get('last_name')
    customer_email = request.args.get('email')
    print("Request is: " + str(request))
    customer = session.query(Customer).filter(Customer.id == customer_id).one()
    #USE IF STATEMENT TO CHECK IF ITEM EXISTS; IF NOT, THEN session.query(CUstomer).filter(Customer.thingy==customer_thingy).one()
    customer_info = { "first_name" : customer.first_name
                    , "last_name" : customer.last_name
                    , "email" : customer.email
                    , "id" : customer.id
                    }
    return flask.jsonify([customer_info]), 200

def add_customer():
    session = Session()
    post = request.get_json()
    if "first_name" not in post or "last_name" not in post:
        return "ERROR: Customer must have first AND last name \n", 404
    customer = Customer(first_name = post["first_name"], last_name=post["last_name"])
    if "email" in post:
        customer.email = post["email"]
    session.add(customer)
    session.commit
    print(post)
    return "Customer successfully added! \n", 201


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
