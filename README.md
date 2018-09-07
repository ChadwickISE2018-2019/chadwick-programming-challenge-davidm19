Overview:

You will implement a simple RESTful API using Flask (http://flask.pocoo.org/docs/0.12/)
and SQLAlchemy (https://www.sqlalchemy.org/).

Getting Started:

A basic implementation has been written to help get you started. You can run it from the
shell inside of the provided vagrant box by navigating to /vagrant and running `python3.6 -m server`.

`cd /vagrant`
`python3.6 -m server`

If you open a second vagrant shell, you should be able to test the end points using the command
line tool `curl`.

Try it:

`curl 'localhost:8888/customer?id=1'`

Tasks:

You will need to modify `server/__main__.py`. In particular, you are implementing the
get_customer, add_customer, and update_customer functions. You will need to be able to handle
all sorts of inputs without resulting in an exception being thrown. Think through the edge
cases during your implementation.

You should only modify the `server/__main__.py` file. When you're finished, send your completed
__main__.py file to joseph.collard@voterlabs.com. When this file was created, an email was sent
marking your start time. Your submission will not be accepted after 4 hours.

Best of luck,

The VoterLabs Team