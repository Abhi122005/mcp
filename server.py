from mcp.server import MCPServer

from database import (
    search_students as search_students_db,
    get_student as get_student_db,
    get_student_marks as get_student_marks_db,
    get_student_attendance as get_student_attendance_db,
    get_low_attendance_students as get_low_attendance_students_db,
    get_student_average_marks as get_student_average_marks_db,
    get_student_performance as get_student_performance_db,
    get_student_attendance_analysis as get_student_attendance_analysis_db
)


mcp = MCPServer("College Assistant")


@mcp.tool()
def search_students(name: str) -> str:
    """Search for students by name and return their student IDs and basic information. Use this when the student's ID is unknown."""

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

    student = get_student_db(student_id)

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
    """Get the subject-wise marks of a student using their student ID."""

    marks = get_student_marks_db(student_id)

    if not marks:
        return "No marks found for this student."

    return "\n".join(
        f"{subject}: {mark}"
        for subject, mark in marks
    )

@mcp.tool()
def get_student_average_marks(student_id: int) -> str:
    """Calculate the average marks of a student across all recorded subjects."""

    average = get_student_average_marks_db(student_id)

    if average is None:
        return "No marks found for this student."

    return f"Average marks: {average:.2f}"

@mcp.tool()
def get_student_attendance(student_id: int) -> str:
    """Get attendance percentage for every subject for a student."""

    attendance = get_student_attendance_db(student_id)

    if not attendance:
        return "No attendance records found for this student."

    return "\n".join(
        f"{subject}: {percentage}%"
        for subject, percentage in attendance
    )

@mcp.tool()
def get_low_attendance_students(threshold: float = 75) -> str:
    """Find students whose subject attendance is below the given percentage."""

    students = get_low_attendance_students_db(threshold)

    if not students:
        return f"No students have attendance below {threshold}%."

    return "\n".join(
        f"{name} - {subject}: {percentage}%"
        for name, subject, percentage in students
    )

@mcp.tool()
def get_student_performance(student_id: int) -> str:
    """Analyze a student's subject-wise marks and identify their strongest and weakest subjects."""

    results = get_student_performance_db(student_id)

    if not results:
        return "No marks found for this student."

    strongest_subject, highest_mark = results[0]
    weakest_subject, lowest_mark = results[-1]

    result = "Subject-wise performance:\n"

    for subject, mark in results:
        result += f"{subject}: {mark}\n"

    result += (
        f"\nStrongest subject: {strongest_subject} ({highest_mark})\n"
        f"Weakest subject: {weakest_subject} ({lowest_mark})"
    )

    return result

@mcp.tool()
def get_student_attendance_analysis(student_id: int) -> str:
    """Analyze a student's subject-wise attendance and identify their highest and lowest attendance."""

    results = get_student_attendance_analysis_db(student_id)

    if not results:
        return "No attendance records found for this student."

    highest_subject, highest_percentage = results[0]
    lowest_subject, lowest_percentage = results[-1]

    result = "Subject-wise attendance:\n"

    for subject, percentage in results:
        result += f"{subject}: {percentage}%\n"

    result += (
        f"\nHighest attendance: "
        f"{highest_subject} ({highest_percentage}%)\n"
        f"Lowest attendance: "
        f"{lowest_subject} ({lowest_percentage}%)"
    )

    return result

@mcp.tool()
def get_student_academic_summary(student_id: int) -> str:
    """Get a complete academic summary for a student using their student ID. This includes marks, average marks, strongest subject, weakest subject, attendance, and lowest attendance."""
    marks = get_student_marks_db(student_id)
    attendance = get_student_attendance_db(student_id)

    if not marks and not attendance:
        return "No academic records found for this student."

    result = "Academic Summary\n\n"

    # Marks
    if marks:
        result += "Marks:\n"

        total = 0

        for subject, mark in marks:
            result += f"- {subject}: {mark}\n"
            total += mark

        average = total / len(marks)

        strongest = max(marks, key=lambda x: x[1])
        weakest = min(marks, key=lambda x: x[1])

        result += f"\nAverage: {average:.2f}\n"
        result += (
            f"Strongest subject: "
            f"{strongest[0]} ({strongest[1]})\n"
        )
        result += (
            f"Weakest subject: "
            f"{weakest[0]} ({weakest[1]})\n"
        )

    # Attendance
    if attendance:
        result += "\nAttendance:\n"

        for subject, percentage in attendance:
            result += f"- {subject}: {percentage}%\n"

        average_attendance = (
            sum(p for _, p in attendance)
            / len(attendance)
        )

        lowest_attendance = min(
            attendance,
            key=lambda x: x[1]
        )

        result += (
            f"\nAverage attendance: "
            f"{average_attendance:.2f}%\n"
        )

        result += (
            f"Lowest attendance: "
            f"{lowest_attendance[0]} "
            f"({lowest_attendance[1]}%)\n"
        )

    return result

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