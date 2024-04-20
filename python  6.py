import sqlite3
from faker import Faker
import random

fake = Faker()

conn = sqlite3.connect('university.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE groups (
                    id INTEGER PRIMARY KEY,
                    name TEXT)''')

cursor.execute('''CREATE TABLE students (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    group_id INTEGER,
                    FOREIGN KEY (group_id) REFERENCES groups(id))''')

cursor.execute('''CREATE TABLE teachers (
                    id INTEGER PRIMARY KEY,
                    name TEXT)''')

cursor.execute('''CREATE TABLE subjects (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    teacher_id INTEGER,
                    FOREIGN KEY (teacher_id) REFERENCES teachers(id))''')

cursor.execute('''CREATE TABLE grades (
                    id INTEGER PRIMARY KEY,
                    student_id INTEGER,
                    subject_id INTEGER,
                    grade INTEGER,
                    date TEXT,
                    FOREIGN KEY (student_id) REFERENCES students(id),
                    FOREIGN KEY (subject_id) REFERENCES subjects(id))''')

conn.commit()

def populate_data():

    groups = ['Group1', 'Group2', 'Group3']
    for group in groups:
        cursor.execute("INSERT INTO groups (name) VALUES (?)", (group,))

    for _ in range(30):
        name = fake.name()
        group_id = random.randint(1, 3)
        cursor.execute("INSERT INTO students (name, group_id) VALUES (?, ?)", (name, group_id))

    for _ in range(3):
        name = fake.name()
        cursor.execute("INSERT INTO teachers (name) VALUES (?)", (name,))

    subjects = [('Math', 1), ('Physics', 2), ('Chemistry', 3), ('Biology', 1), ('History', 2)]
    for subject in subjects:
        cursor.execute("INSERT INTO subjects (name, teacher_id) VALUES (?, ?)", subject)

    for student_id in range(1, 31):
        for subject_id in range(1, 6):
            grade = random.randint(1, 100)
            date = fake.date()
            cursor.execute("INSERT INTO grades (student_id, subject_id, grade, date) VALUES (?, ?, ?, ?)",
                           (student_id, subject_id, grade, date))

    conn.commit()

populate_data()
SELECT s.name AS student_name, AVG(g.grade) AS average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id
ORDER BY AVG(g.grade) DESC
LIMIT 5;

