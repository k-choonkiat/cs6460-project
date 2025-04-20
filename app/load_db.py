from database import Database
# schema is id, first name, last name, email, age
students = [
            (1, "John", "Wick", "johnwick@test.com", 14),
            (2, "David", "Goh", "davidgoh@test.com", 13),
            (3, "Zack", "Synder", "zacksynder@test.com", 12)
            ]

db = Database()
for student in students:
    db.add_students(student)


        