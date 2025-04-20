import pathlib
import sqlite3
import csv

DATABASE_PATH = r"C:\Users\choon\CS6460-app\app\database\reading_app.db"

class Database:
    def __init__(self, db_path=DATABASE_PATH):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()
        self.cursor.execute("PRAGMA foreign_keys = 1")
        self._create_students()
        self._create_books()
        self._create_reviews()
        self._create_readingHistory()
        self._create_forumPosts()
        self._create_forumReplies()

    def _create_students(self):
        query = """
            CREATE TABLE IF NOT EXISTS students(
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                age INTEGER,
                points INTEGER
            );
        """
        self._run_query(query)
    def _create_books(self):
        query = """
            CREATE TABLE IF NOT EXISTS books(
                id INTEGER PRIMARY KEY,
                title TEXT,
                description TEXT,
                author TEXT,
                image_url TEXT,
                genre TEXT
            );
        """
        self._run_query(query)

    def _create_reviews(self):
        query = """
            CREATE TABLE IF NOT EXISTS reviews(
                id INTEGER PRIMARY KEY,
                author TEXT,
                review TEXT,
                book TEXT,
                rating INTEGER
            );
        """
        self._run_query(query)

    def _create_readingHistory(self):
        query = """
            CREATE TABLE IF NOT EXISTS readingHistory(
                id INTEGER PRIMARY KEY,
                student_id INTEGER,
                book_id INTEGER,
                rating INTEGER,
                review TEXT,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (book_id) REFERENCES books(id)
            );
        """
        self._run_query(query)

    def _create_forumPosts(self):
        query = """
            CREATE TABLE IF NOT EXISTS forumPosts(
                id INTEGER PRIMARY KEY,
                student_id INTEGER,
                votes INTEGER,
                topic TEXT,
                post TEXT,
                FOREIGN KEY (student_id) REFERENCES students(id)
            );
        """
        self._run_query(query)

    def _create_forumReplies(self):
        query = """
            CREATE TABLE IF NOT EXISTS forumReplies(
                id INTEGER PRIMARY KEY,
                post_id INTEGER,
                student_id INTEGER,
                votes INTEGER,
                reply TEXT,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (post_id) REFERENCES formuPosts(id)
            );
        """
        self._run_query(query)

    def _run_query(self, query, *query_args):
        result = self.cursor.execute(query, [*query_args])
        self.db.commit()
        return result
    
    def add_students(self, contact):
        self._run_query(
            "INSERT INTO students VALUES (?, ?, ?, ?, ?, ?);",
            *contact,
        )

    def add_books(self, books):
        self._run_query(
            "INSERT INTO books VALUES (?, ?, ?, ?, ?, ?);",
            *books,
        )

    def add_books_to_history(self, books):
        self._run_query(
            "INSERT INTO readingHistory VALUES (?, ?, ?, ?, ?);",
            *books,
        )

    def add_forumPosts(self, post):
        self._run_query(
            "INSERT INTO forumPosts VALUES ( ?, ?, ?, ?, ?);",
            *post,
        )
    def add_formuReplies(self, reply):
        self._run_query(
            "INSERT INTO forumReplies VALUES ( ?, ?, ?, ?, ?);",
            *reply,
        )

    def get_all_students(self):
        result = self._run_query("SELECT * FROM students;")
        return result.fetchall()

    def get_all_books(self):
        result = self._run_query("SELECT * FROM books;")
        return result.fetchall()

    def get_all_reviews(self):
        result = self._run_query("SELECT * FROM reviews;")
        return result.fetchall()

    def get_all_reading_history(self):
        result = self._run_query("SELECT * FROM readingHIstory;")
        return result.fetchall()
    
    def get_all_forumPost(self):
        result = self._run_query("SELECT * FROM forumPosts;")
        return result.fetchall()
    
    def get_all_forumReplies(self):
        result = self._run_query("SELECT * FROM forumReplies;")
        return result.fetchall()


        #load books data from csv
        # with open('books_data_cleaned.csv','r',encoding="utf8") as fin:
        #     dr = csv.DictReader(fin)
        #     to_db = [(i['id'], i['title'],i['description'],i['author'],i['image_url'],i['genre']) for i in dr]
        # self.cursor.executemany("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?);", to_db)