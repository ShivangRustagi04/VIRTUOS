import sqlite3
conn = sqlite3.connect('assignment.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS INTERVIEW (
               StudentName TEXT,
               CollegeName TEXT,
               Round1Marks FLOAT,
               Round2Marks FLOAT,
               Round3Marks FLOAT,
               TechnicalRoundMarks FLOAT,
               TotalMarks FLOAT,
               Result TEXT,
               Rank INTEGER)
''')
conn.commit()

StudentName = input("Enter Student Name: ")
if len(StudentName) > 30:
    print("Error: Student Name must be less then 30 characters.")
    exit()

CollegeName = input("Enter College Name: ")
if len(CollegeName) > 50:
    print("Error: College Name must be less then 50 characters.")
    exit()

try:
    Round1Marks = float(input("Enter Round 1 Marks (out of 10): "))
    if Round1Marks < 0 or Round1Marks > 10:
        print("Error: Round 1 Marks must be between 0 and 10.")
        exit()
except ValueError:
    print("Error: Invalid input for Round 1 Marks.")
    exit()

try:
    Round2Marks = float(input("Enter Round 2 Marks (out of 10): "))
    if Round2Marks < 0 or Round2Marks > 10:
        print("Error: Round 2 Marks must be between 0 and 10.")
        exit()

except ValueError:
    print("Error: Invalid input for Round 2 Marks.")
    exit()

try:
    Round3Marks = float(input("Enter Round 3 Marks (out of 10): "))
    if Round3Marks < 0 or Round3Marks > 10:
        print("Error: Round 3 Marks must be between 0 and 10.")
        exit()

except ValueError:
    print("Error: Invalid input for Round 3 Marks.")
    exit()

try:
    TechnicalRoundMarks = float(input("Enter Technical Round Marks (out of 20): "))
    if TechnicalRoundMarks < 0 or TechnicalRoundMarks > 20:
        print("Error: Technical Round Marks must be between 0 and 20.")
        exit()

except ValueError:
    print("Error: Invalid input for Technical Round Marks.")
    exit()

total_marks = Round1Marks + Round2Marks + Round3Marks + TechnicalRoundMarks

try:
    if total_marks < 0 or total_marks > 50:
        print("Error: Total Marks must be between 0 and 50.")
        exit()

except ValueError:
    print("Error: Invalid input for Total Marks.")
    exit()

result = "SELECTED" if total_marks >= 35 else "REJECTED"

cursor.execute('''
INSERT INTO INTERVIEW (StudentName, CollegeName, Round1Marks, Round2Marks, Round3Marks, TechnicalRoundMarks, TotalMarks, Result)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
               (StudentName, CollegeName, Round1Marks, Round2Marks, Round3Marks, TechnicalRoundMarks, total_marks, result))
conn.commit()

print("\nResult details:")
cursor.execute('SELECT * FROM INTERVIEW ORDER BY TotalMarks DESC')
rows = cursor.fetchall()

rank = 1
prev_marks = None
for idx, row in enumerate(rows):
    if prev_marks is not None and row[6] == prev_marks:
        pass
    else:
        rank = idx + 1
    cursor.execute('UPDATE INTERVIEW SET Rank = ? WHERE StudentName = ? AND CollegeName = ?', (rank, row[0], row[1]))
    conn.commit()
    print(f"Student Name: {row[0]}, College Name: {row[1]}, Round 1 Marks: {row[2]}, Round 2 Marks: {row[3]}, Round 3 Marks: {row[4]}, Technical Round Marks: {row[5]}, Total Marks: {row[6]}, Result: {row[7]}, Rank: {rank}")
    prev_marks = row[6]
conn.close()
