from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
from flask_app import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
db = "mundane_arcane"
class Mundane:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.description = db_data['description']
        self.price = db_data['price']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.creator = None
    @classmethod 
    def get_all(cls):
        query = "SELECT * From mundanes JOIN users ON users.id = mundanes.user_id;"
        result = connectToMySQL(db).query_db(query)
        mundanes = []
        for row in result:
            this_mundanes= cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_mundanes.creator = user.User(user_data)
            mundanes.append(this_mundanes)
        return mundanes
    
    @classmethod 
    def get_all_by_id(cls,data):
        query = """
                SELECT * FROM mundanes
                LEFT JOIN users
                ON users.id = mundanes.user_id
                WHERE users.id = %(id)s;
                """
        results = connectToMySQL(db).query_db(query,data)
        return results
    
    @classmethod 
    def get_by_id(cls,data):
        query = """
                SELECT * FROM mundanes
                WHERE id = %(id)s;
                """
        results = connectToMySQL(db).query_db(query,data)
        return results[0]
    @classmethod 
    def save(cls, form_data):
        query = """
                INSERT INTO mundanes (name, description,price, user_id)
                VALUES (%(name)s,%(description)s,%(price)s,%(user_id)s);
                """
        return connectToMySQL(db).query_db(query,form_data)


    @classmethod
    def destroy(cls,data):
        query = """
                DELETE FROM mundanes
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,data)
    
    @staticmethod 
    def validate_mund(form_data):
        is_valid = True

        if len(form_data['name']) < 3:
            flash("title should have at least 3 characters.")
            is_valid = False
        if len(form_data['description']) < 10:
            flash("description must be at least 10 characters long.")
            is_valid = False
            
        return is_valid
    
