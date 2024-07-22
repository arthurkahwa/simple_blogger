from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import logging
from pydantic import BaseModel

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DATABASE_CONFIG = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres'
}


class Post(BaseModel):
    title: str
    post: str | None = None


app = FastAPI()


# Get database connection
def get_database_connection():
    try:
        connection = psycopg2.connect(**DATABASE_CONFIG)
        connection.autocommit = True
        return connection
    except psycopg2.OperationalError as e:
        logger.error("Database connection error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Get all blog posts
@app.get("/posts/")
async def get_all_posts():
    try:
        db_connection = get_database_connection()
        cursor = db_connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT * FROM simple_blog
        """)
        all_posts = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return json.loads(json.dumps(all_posts, default=str))
    except psycopg2.Error as error:
        raise HTTPException(status_code=500, detail="Error retrieving data {error}")


# Get a single blog post
@app.get("/posts/{post_id}")
async def get_single_post(post_id):
    try:
        db_connection = get_database_connection()
        cursor = db_connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT * FROM simple_blog 
            WHERE id = %s
                """, (post_id, ))
        post = cursor.fetchone()
        if post is None:
            raise HTTPException(status_code=404, detail="Item with id {post_id} not found")
        cursor.close()
        db_connection.close()
        return json.loads(json.dumps(post, default=str))
    except psycopg2.Error as error:
        raise HTTPException(status_code=500, detail="Error retrieving data")


# Create a blog post
@app.post("/posts/")
async def create_post(post: Post):
    try:
        db_connection = get_database_connection()
        cursor = db_connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
        INSERT INTO simple_blog (title, post)
        VALUES (%s, %s)
        """, (post.title, post.post))
        cursor.close()
        db_connection.close()
        return {"message": "Post created: "}
    except psycopg2.Error as error:
        raise HTTPException(status_code=500, detail="Error creating data: " + str(error))


# Update a single blog post
@app.put("/posts/{post_id}")
async def update_post(post_id: int, post: Post):
    try:
        db_connection = get_database_connection()
        cursor = db_connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
         UPDATE simple_blog 
         SET title = %s, post = %s
         WHERE id = %s
        """, (post.title, post.post, post_id))
        cursor.close()
        db_connection.close()
        return {"message": "Post updated: "}
    except psycopg2.Error as error:
        raise HTTPException(status_code=500, detail="Error creating data: " + str(error))

# Delete a blog post
@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    try:
        db_connection = get_database_connection()
        cursor = db_connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            DELETE FROM simple_blog 
            WHERE id = %s
                """, (post_id, ))
        cursor.close()
        db_connection.close()
        return {"message": "Post deleted: "}
    except psycopg2.Error as error:
        raise HTTPException(status_code=500, detail="Error deleting data")
