from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Show:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.shows_id = data['shows_id']
        self.num_of_likes = 0;

    @classmethod
    def get_all_shows(cls, data):
        query = "SELECT * FROM shows JOIN users ON users.id = shows.user_id LEFT JOIN (SELECT * FROM likes WHERE users_id = %(user_id)s) as likes ON likes.shows_id = shows.id;"
        results = connectToMySQL('exam1_schema').query_db(query, data)
        shows = []
        for item in results:
            new_show = cls(item)
            new_user_data = {
                'id' : item['users.id'],
                'first_name' : item['first_name'],
                'last_name' : item['last_name'],
                'email' : item['email'],
                'password' : item['password'],
                'created_at' : item['users.created_at'],
                'updated_at' : item['users.updated_at'],
                'shows_id' : item['shows_id']
            }
            new_user = user.User(new_user_data)
            new_show.user = new_user
            shows.append(new_show)

        return shows

    @classmethod
    def create_new_show(self, data):
        query = "INSERT INTO shows (title, network, release_date, description, user_id) VALUES(%(title)s,%(network)s,%(release_date)s,%(description)s,%(user_id)s);"
        result = connectToMySQL('exam1_schema').query_db(query, data)
        return result


    @staticmethod
    def validate_show(data):
        is_valid = True

        if len(data['title']) < 3:
            is_valid = False
            flash("Show name needs to be greater than 3 characters")

        if len(data['network']) < 3:
            is_valid = False
            flash("Show network needs to be greater than 3 characters")
        
        if len(data['release_date']) != 10:
            is_valid = False
            flash("Please insure theres is a release date")

        if len(data['description']) < 3:
            is_valid = False
            flash("Show description needs to be greater than 3 characters")

        return is_valid

    @classmethod
    def view_description(cls, data):
        query = "SELECT * FROM shows JOIN users ON shows.user_id = users.id LEFT JOIN likes ON shows.id = likes.shows_id WHERE shows.id = %(shows_id)s;"
        result = connectToMySQL('exam1_schema').query_db(query, data)
        single_show = cls(result[0])
        like = 0;
        for item in result:
            if item['shows_id']:
                like += 1;
        single_show.num_of_likes += like;

        return single_show

    @classmethod
    def update_show(cls,data):
        query = "UPDATE shows SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s WHERE shows.id = %(id)s;"
        connectToMySQL('exam1_schema').query_db(query, data)

    @classmethod
    def delete_show(cls, data):
        query = "DELETE FROM shows WHERE id = %(id)s;"
        connectToMySQL('exam1_schema').query_db(query, data)

    @classmethod
    def add_like(cls, data):
        query = "INSERT INTO likes(users_id, shows_id) SELECT %(users_id)s, %(shows_id)s WHERE  NOT EXISTS (SELECT * FROM likes WHERE users_id = %(users_id)s and shows_id = %(shows_id)s);"
        result = connectToMySQL('exam1_schema').query_db(query, data)
        return result

    @classmethod
    def delete_like(cls,data):
        query = "DELETE FROM likes WHERE users_id= %(users_id)s AND shows_id= %(shows_id)s;"
        result = connectToMySQL('exam1_schema').query_db(query, data)
        return result
