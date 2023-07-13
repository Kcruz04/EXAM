# import the function that will return an instance of a connection
from exam_app.config.mysqlconnection import connectToMySQL
from exam_app.models import tv_show_model
from flask import flash
from exam_app import DATABASE, app, BCRYPT
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 


class User:
    db = 'exam_schema'
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.tv_shows = []
    # Now we use class methods to query our database

    @classmethod
    def users_with_tv_shows( cls , id):
        data = {"id":id}
        query = "SELECT * FROM users LEFT JOIN tv_shows ON tv_shows.users_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db( query , data )
        # results will be a list of topping objects with the burger attached to each row. 
        user = cls( results[0] )
        tv_shows = []
        for row_from_db in results:
            # Now we parse the ninja data to make instances of ninjas and add them into our list.
            tv_show_data = {  
                "id" : row_from_db["tv_shows.id"],
                "title" : row_from_db["title"],
                "network" : row_from_db["network"],
                "release_date" : row_from_db["release_date"],
                "description" : row_from_db["description"],
                "created_at" : row_from_db["tv_shows.created_at"],
                "updated_at" : row_from_db["tv_shows.updated_at"],
                "user_id" : row_from_db["user_id"]
            }
        tv_shows.append(tv_show_model.Tv_show(tv_show_data ) )
        usertv_shows =tv_shows
        return user

    @classmethod
    def save(cls, data ):
        query = """INSERT INTO users ( first_name , last_name , email , password, created_at, updated_at ) 
        VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s , NOW() , NOW() );"""
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db).query_db( query, data )
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db).query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append( cls(user) )
        return users
    
    
    @classmethod
    def get_one(cls, id):
        data = {
            "id" : id
        }
        query = """
            SELECT * FROM users
            WHERE id = %(id)s;
        """
        connectToMySQL(cls.db).query_db( query, data )
        results = connectToMySQL(cls.db).query_db( query, data )
        user = cls(results[0])
        return user
    
    @classmethod
    def validate(cls, form):
        is_valid = True # we assume this is true
        if len(form['first_name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(form['email']):
            flash('invalid email')
            is_valid = False
        elif cls.get_by_email(form['email']):
            flash('email already registered')
        if form['password'] != form['confirm_password']:
            flash('passwords do not match')
            is_valid = False
        return is_valid

    @classmethod
    def register(cls, form):
        

        hash = BCRYPT.generate_password_hash( form['password'])
        print(hash)
        query = """INSERT INTO users ( first_name , last_name , email , password ) 
        VALUES ( %(first_name)s , %(last_name)s , %(email)s ,%(password)s);"""
        # data is a dictionary that will be passed into the save method from server.py
        form = {
            **form,
            "password" : hash
        }
        return connectToMySQL(cls.db).query_db( query, form )
    
    @classmethod
    def get_by_email(cls, email):
        data = {
            'email' : email
        }

        query = """
        SELECT * FROM users
        WHERE email = %(email)s
        """
        results = connectToMySQL(cls.db).query_db( query, data)
    
        if results:
            return cls(results[0])

        else:
            return False

    @classmethod
    def login(cls, form):
        valid_email = cls.get_by_email(form['email'])
        if valid_email:
            if BCRYPT.check_password_hash( valid_email.password, form['password']):
                return valid_email
            else:
                flash('Invalid password')
                return False
        else:
            flash("Invalid email!")
            return False