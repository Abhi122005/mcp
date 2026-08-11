import sqlite3

DATABASE_NAME = "college.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            semester INTEGER NOT NULL,
            section TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            marks REAL NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            percentage REAL NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)

    connection.commit()
    connection.close()


def insert_sample_data():
    connection = get_connection()
    cursor = connection.cursor()

    students = [
        ("Abhishek", "abhishek@example.com", "Computer Science", 4, "D"),
        ("Rahul", "rahul@example.com", "Computer Science", 4, "D"),
        ("Arjun", "arjun@example.com", "Computer Science", 4, "C")
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO students
        (name, email, department, semester, section)
        VALUES (?, ?, ?, ?, ?)
    """, students)

    cursor.execute("SELECT id, name FROM students")

    student_ids = {
        name: student_id
        for student_id, name in cursor.fetchall()
    }

    marks = [
        (student_ids["Abhishek"], "DBMS", 92),
        (student_ids["Abhishek"], "AI", 88),
        (student_ids["Abhishek"], "Operating Systems", 85),

        (student_ids["Rahul"], "DBMS", 78),
        (student_ids["Rahul"], "AI", 81),
        (student_ids["Rahul"], "Operating Systems", 74),

        (student_ids["Arjun"], "DBMS", 95),
        (student_ids["Arjun"], "AI", 91),
        (student_ids["Arjun"], "Operating Systems", 89)
    ]

    cursor.executemany("""
        INSERT INTO marks
        (student_id, subject, marks)
        VALUES (?, ?, ?)
    """, marks)

    attendance = [
        (student_ids["Abhishek"], "DBMS", 92),
        (student_ids["Abhishek"], "AI", 88),
        (student_ids["Abhishek"], "Operating Systems", 85),

        (student_ids["Rahul"], "DBMS", 72),
        (student_ids["Rahul"], "AI", 68),
        (student_ids["Rahul"], "Operating Systems", 74),

        (student_ids["Arjun"], "DBMS", 96),
        (student_ids["Arjun"], "AI", 94),
        (student_ids["Arjun"], "Operating Systems", 91)
    ]

    cursor.executemany("""
        INSERT INTO attendance
        (student_id, subject, percentage)
        VALUES (?, ?, ?)
    """, attendance)

    connection.commit()
    connection.close()


def search_students(name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, email, department, semester, section
        FROM students
        WHERE name LIKE ?
    """, (f"%{name}%",))

    students = cursor.fetchall()

    connection.close()

    return students


def get_student(student_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, email, department, semester, section
        FROM students
        WHERE id = ?
    """, (student_id,))

    student = cursor.fetchone()

    connection.close()

    return student


def get_student_marks(student_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT subject, marks
        FROM marks
        WHERE student_id = ?
    """, (student_id,))

    marks = cursor.fetchall()

    connection.close()

    return marks


def get_student_attendance(student_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT subject, percentage
        FROM attendance
        WHERE student_id = ?
    """, (student_id,))

    attendance = cursor.fetchall()

    connection.close()

    return attendance


def get_low_attendance_students(threshold):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            students.name,
            attendance.subject,
            attendance.percentage
        FROM attendance
        JOIN students
        ON attendance.student_id = students.id
        WHERE attendance.percentage < ?
        ORDER BY attendance.percentage ASC
    """, (threshold,))

    results = cursor.fetchall()

    connection.close()

    return results

def get_student_average_marks(student_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT AVG(marks)
        FROM marks
        WHERE student_id = ?
    """, (student_id,))

    result = cursor.fetchone()

    connection.close()

    return result[0] if result and result[0] is not None else None

def get_student_performance(student_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT subject, marks
        FROM marks
        WHERE student_id = ?
        ORDER BY marks DESC
    """, (student_id,))

    results = cursor.fetchall()

    connection.close()

    return results

def get_student_attendance_analysis(student_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT subject, percentage
        FROM attendance
        WHERE student_id = ?
        ORDER BY percentage DESC
    """, (student_id,))

    results = cursor.fetchall()

    connection.close()

    return results

if __name__ == "__main__":
    create_tables()
    insert_sample_data()
    print("Database initialized successfully.")