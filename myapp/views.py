from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
from datetime import datetime
from myapp.database import Database
from . import app
import os

def get_db_connection():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'database', 'reading_app.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/", methods=['GET', 'POST'])
def search():
    query = request.form.get("book_searched")
    books = []

    conn = get_db_connection()
    if query:
        # print(query)
        cursor = conn.execute('SELECT * from books WHERE title lIKE ?', ['%' + query +'%'])
        books = cursor.fetchall()
    else:
        books = conn.execute('SELECT * from books where id <> 1 LIMIT 30 ').fetchall()
    # print(query)
    conn.close()
    return render_template("search.html", books = books)

@app.route("/submit_review", methods=["POST"])
def submit_review():
    try:
        book_id = request.form.get('book_id')
        review = request.form.get('review')
        rating = request.form.get(f'rating_{book_id}')
        student_id = 1
        print(f"Received book ID: {book_id}")
        print(f"Received rating: {rating}")
        print(f"Review: {review}")

        if ( not review ) or ( not rating ):
            return jsonify({"success": False, "message": "Missing required fields."})
        conn = get_db_connection()
        conn.execute("INSERT INTO readingHistory (student_id, book_id, rating, review, votes) VALUES (?, ?, ?, ?, 0)", (student_id, book_id, rating, review))
        conn.commit()
        conn.close()

        return redirect("/")
    except Exception as e:
        return str(e), 500


@app.route("/profile/")
def profile():
    history = []

    conn = get_db_connection()
    cursor = conn.execute('SELECT * from readingHistory t1 LEFT JOIN books t2 on t1.book_id = t2.id LIMIT 1')
    history = cursor.fetchall()
    print(history)
    conn.close()
    return render_template("profile.html", history = history)

@app.route("/reward/")
def reward():
    rewards = [
        {
            'id': 1,
            'name': 'Custom Bookmark',
            'description': 'A beautiful handmade bookmark to mark your adventures.',
            'points': 50,
            'image_url': '/static/bookmark.png'
        },
        {
            'id': 2,
            'name': 'Classic Novel',
            'description': 'Choose a book from our classic collection.',
            'points': 150,
            'image_url': '/static/animal_farm.jpg'
        },
        {
            'id': 3,
            'name': 'Seasonal Bookmark',
            'description': 'Seasonal bookmarks that are only for this period.',
            'points': 200,
            'image_url': '/static/bookmark-2.png'
        }
    ]
    return render_template('reward.html', rewards=rewards)

@app.route("/forum" , methods=["GET","POST"])
def forum():
    if request.method == "POST":
        post_topic = request.form['forum_post_topic']
        post = request.form['forum_post']
        if ( not post_topic ) or ( not post ):
            return jsonify({"success": False, "message": "Missing required fields."})
        conn = get_db_connection()
        conn.execute("INSERT INTO forumPosts (student_id, votes, topic, post) VALUES (1, 0, ?, ?)", (post_topic, post))
        conn.commit()
        conn.close()

        return redirect("/forum")

    conn = get_db_connection()
    cursor = conn.execute('SELECT * from forumPosts t1 LEFT JOIN students t2 on t1.student_id = t2.id ORDER BY t1.id desc ')
    posts = cursor.fetchall()
    posts_with_replies = []
    for post in posts:
        post_id = post['id']
        cursor = conn.execute("SELECT * FROM forumReplies t1 LEFT JOIN students t2 on t1.student_id = t2.id WHERE post_id = ? " , (post_id,))
        replies = [dict(row) for row in cursor.fetchall()]
        posts_with_replies.append({
            'id': post['id'],
            'topic' : post['topic'],
            'post' : post['post'],
            'votes' : post['votes'],
            'replies' : replies
        })
    conn.close()
    return render_template("forum.html", posts = posts_with_replies)

@app.route("/submit_reply", methods=["POST"])
def submit_reply():
    try:
        student_id = request.form.get('student_id')
        post_id = request.form.get('post_id')
        reply = request.form.get('reply')

        if ( not reply ):
            return jsonify({"success": False, "message": "Missing required fields."})
        conn = get_db_connection()
        conn.execute("INSERT INTO forumReplies (post_id, student_id, votes, reply) VALUES (?, ?, 0, ?)", (post_id, student_id, reply))
        conn.commit()
        conn.close()

        return redirect("/forum")
    except Exception as e:
        return str(e), 500

@app.route("/events/")
def events():
    return render_template("events.html")

@app.route("/review/")
def review():
    reviews = []

    conn = get_db_connection()
    cursor = conn.execute('SELECT * from readingHistory t1 LEFT JOIN books t2 on t1.book_id = t2.id ORDER BY t1.book_id desc ')
    reviews = cursor.fetchall()
    conn.close()
    return render_template("review.html", reviews = reviews)

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

@app.route('/vote/<int:review_id>', methods=['POST'])
def vote(review_id):
    conn = get_db_connection()
    delta = request.json.get('delta', 0)
    # print('delta is ' + str(delta))
    # print('review id is ' + str(review_id))
    conn.execute('UPDATE readingHistory SET votes = votes + ? WHERE id = ?', (delta, review_id))
    conn.commit()
    new_votes = conn.execute('SELECT votes FROM readingHistory WHERE id = ?', (review_id,)).fetchone()
    conn.close()
    if new_votes:
         return jsonify({"success": True, "new_votes": new_votes["votes"]})
    return jsonify({"success": False, "error": "Post not found"}), 404

@app.route('/rewards/<int:reward_id>')
def redeem_reward(reward_id):
    # Normally you'd fetch this from a database
    reward = get_reward_by_id(reward_id)
    user_points = get_user_points(current_user.id)  # however you're tracking points
    return render_template('redeem_reward.html', reward=reward, user_points=user_points)


@app.route('/read/<filename>')
def read_pdf(filename):
    if not filename.endswith('.pdf'):
        return "Unsupported file type", 400
    base_dir = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(base_dir, 'static', 'files', filename)
    if not os.path.exists(filepath):
        return "File not found", 404

    return render_template('read_pdf_js.html', filename=filename)
    


