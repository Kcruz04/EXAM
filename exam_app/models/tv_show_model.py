# import the function that will return an instance of a connection
from exam_app.config.mysqlconnection import connectToMySQL
from exam_app.models import user_model

class Tv_show:
    db = 'exam_schema'
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database

    @classmethod
    def tv_shows_with_users( cls ):
        query = "SELECT * FROM tv_shows JOIN users ON tv_shows.user_id = users.id ;"
        results = connectToMySQL(cls.db).query_db( query)
        # results will be a list of topping objects with the users attached to each row. 
        tv_shows = []
        if results:
            for row_from_db in results:
                
                tv_show = Tv_show(row_from_db)
                # Now we parse the tv_shows data to make instances of tv_shows and add them into our list.
                user_data = {  
                    "id" : row_from_db["users.id"],
                    "first_name" : row_from_db["first_name"],
                    "last_name" : row_from_db["last_name"],
                    "password" : row_from_db["password"],
                    "email" : row_from_db["email"],
                    "created_at" : row_from_db["users.created_at"],
                    "updated_at" : row_from_db["users.updated_at"],
                }
                user = user_model.User(user_data)
                tv_show.user = user
                tv_shows.append(tv_show)
        return tv_shows

    @classmethod
    def save(cls, data):

        query = """INSERT INTO tv_shows ( title , network , release_date , description, user_id ) 
        VALUES ( %(title)s , %(network)s , %(release_date)s , %(description)s , %(user_id)s ) ;"""
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db).query_db( query, data )
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM tv_shows;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db).query_db(query)
        # Create an empty list to append our instances of tv_shows
        tv_shows = []
        # Iterate over the db results and create instances of tv_shows with cls.
        for tv_show in results:
            tv_shows.append( cls(tv_show) )
        return tv_shows
    
    @classmethod
    def get_one(cls, id):
        data = {
            "id" : id
        }
        query = """
            SELECT * FROM tv_shows
            WHERE id = %(id)s;
        """
        connectToMySQL(cls.db).query_db( query, data )
        results = connectToMySQL(cls.db).query_db( query, data )
        tv_show = cls(results[0])
        return tv_show
    
    @classmethod
    def update(cls, data):
        query = """
        UPDATE tv_shows
        SET
        title = %(title)s,
        network = %(network)s,
        release_date = %(release_date)s,
        description = %(description)s
        WHERE id = %(id)s;
        """
        connectToMySQL(cls.db).query_db( query, data )

    @classmethod
    def delete(cls,id):
        data = {
            "id" : id
        }
        query = """
        DELETE FROM tv_shows
        WHERE id=%(id)s;
        """
        return connectToMySQL(cls.db).query_db( query, data )