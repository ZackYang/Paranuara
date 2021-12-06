# Readme

> This is my first attempt to develop an API using Python, Flask and
> MongoDB. A lot of the designs look still very primitive.


# Requirements and Installation

Python >= 3.9
MongoDB >= 5.0.0

## Download project

    $ cd ~/
    $ git clone git@github.com:ZackYang/Paranuara.git
    $ cd Paranuara

## Install required libraries 

    $ pip install -r requirements.txt

## Load data in to database from json files

    $ python3 setup.py

## Start Server

    $ flask run
This server will listen to port **localhost:5000**

## Run Testing
		
    $ python3 -m unittest tests/unit_tests.py
    $ python3 -m unittest tests/request_tests.py

# API docs

## Companies APIs

You can use both index and company name as the Identity

    http://localhost:5000/api/companies/<string:name>
    or
    http://localhost:5000/api/companies/<int:id>
### For example:

http://localhost:5000/api/companies/99
http://localhost:5000/api/companies/STRALUM

## Friends in common APIs

You can use both index and company name as the Identity

    http://localhost:5000/api/friends_in_common/<int:a_id>-<int:b_id>/with/<string:color>/eyes
### For example:

http://localhost:5000/api/friends_in_common/99-101/with/brown/eyes
http://localhost:5000/api/friends_in_common/94-102/with/blue/eyes

No friends in common
http://localhost:5000/api/friends_in_common/92-102/with/brown/eyes

## Person APIs

    http://localhost:5000/api/people/<int:id>

### For example:
http://localhost:5000/api/people/5
