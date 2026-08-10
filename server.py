from mcp.server import MCPServer

from database import (
    search_students as search_students_db,
    get_student as db_get_student,
    get_student_marks as db_get_student_marks,
    get_student_attendance as db_get_student_attendance,
    get_low_attendance_students as db_get_low_attendance_students
)


mcp = MCPServer("College Assistant")


@mcp.tool()
def search_students(name: str) -> str:
    """Search for students by name."""

    students = search_students_db(name)

    if not students:
        return "No students found."

    if len(students) == 1:
        student = students[0]

        student_id, student_name, email, department, semester, section = student

        return (
            f"ID: {student_id}\n"
            f"Name: {student_name}\n"
            f"Email: {email}\n"
            f"Department: {department}\n"
            f"Semester: {semester}\n"
            f"Section: {section}"
        )

    result = "Multiple students found:\n"

    for student in students:

        student_id, student_name, email, department, semester, section = student

        result += (
            f"ID: {student_id} | "
            f"Name: {student_name} | "
            f"Email: {email} | "
            f"Department: {department} | "
            f"Semester: {semester} | "
            f"Section: {section}\n"
        )

    return result

@mcp.tool()
def get_student(student_id: int) -> str:
    """Get detailed information about a student using their ID."""

    student = db_get_student(student_id)

    if not student:
        return "Student not found."

    student_id, name, email, department, semester, section = student

    return (
        f"ID: {student_id}\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Department: {department}\n"
        f"Semester: {semester}\n"
        f"Section: {section}"
    )

@mcp.tool()
def get_student_marks(student_id: int) -> str:
    """Get all subject marks for a student."""

    marks = db_get_student_marks(student_id)

    if not marks:
        return "No marks found for this student."

    results = []

    for subject, mark in marks:
        results.append(f"{subject}: {mark}")

    return "\n".join(results)

@mcp.tool()
def get_student_attendance(student_id: int) -> str:
    """Get attendance percentage for every subject for a student."""

    attendance = db_get_student_attendance(student_id)

    if not attendance:
        return "No attendance records found for this student."

    results = []

    for subject, percentage in attendance:
        results.append(f"{subject}: {percentage}%")

    return "\n".join(results)

@mcp.tool()
def get_low_attendance_students(threshold: float = 75) -> str:
    """Find students whose subject attendance is below the given percentage."""

    students = db_get_low_attendance_students(threshold)

    if not students:
        return "No students found below the attendance threshold."

    results = []

    for name, subject, percentage in students:
        results.append(
            f"{name} - {subject}: {percentage}%"
        )

    return "\n".join(results)

@mcp.resource("college://information")
def college_information() -> str:
    """General information about the college."""

    return """
College Information

Department:
Computer Science and Engineering

Available Semesters:
1, 2, 3, 4, 5, 6, 7, 8

Available Student Information:
- Student profile
- Marks
- Attendance

Available Assistant Capabilities:
- Search students
- View student details
- View student marks
- View student attendance
- Find students with low attendance
"""
@mcp.prompt()
def student_summary(student_name: str) -> str:
    """Create a structured prompt for analyzing a student's academic performance."""

    return f"""
You are a college academic assistant.

Prepare a concise academic summary for the student: {student_name}.

Include:
1. Student profile
2. Subject-wise marks
3. Subject-wise attendance
4. Any attendance below 75%
5. Overall academic observations

Use the available MCP tools to retrieve the required information.
Do not invent any information that is not available.
"""

if __name__ == "__main__":
    mcp.run()