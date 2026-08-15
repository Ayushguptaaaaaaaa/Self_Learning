import json, os, argparse, functools

DATA_FILE = os.path.join(os.path.dirname(__file__), "students.json")

SUBJECTS = ["Math", "Science", "English", "History", "Computer Science"]

GRADE_SLABS = [
    (90, "A"),
    (80, "B"),
    (70, "C"),
    (60, "D"),
    (50, "E"),
    (40, "F"),
    (0,  "FAIL"),
]

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"students": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_grade(score):
    for threshold, letter in GRADE_SLABS:
        if score >= threshold:
            return letter
    return "FAIL"

class Student:
    def __init__(self, name, scores):
        self.name = name
        self.scores = scores 

        self.grades = {}
        for subject, score in self.scores.items():
            self.grades[subject] = get_grade(score)

        # compute overall average
        self.average = sum(self.scores.values()) / len(self.scores) 

    def __str__(self):
        subject_lines = ""
        for subject, score in self.scores.items():
            subject_lines += f"  {subject}: {score} ({self.grades    [subject]})\n"
        return (
            f"Student: {self.name}\n"
            f"Average: {self.average:.1f} ({get_grade(self.    average)})\n"
            f"Scores:\n{subject_lines}"
        )

    def __len__(self):
        return len(self.scores)

    def __contains__(self, subject):
        return subject in self.scores

    def to_dict(self):
        return {
            "name": self.name,
            "scores": self.scores
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["scores"])


class StudentReport:
    def __init__(self):
        data = load_data()
        self.students = [Student.from_dict(s) for s in data["students"]]

    
    def add_student(self, name, scores):
        student = Student(name, scores)
        self.students.append(student)
        save_data({"students": [s.to_dict() for s in self.    students]})

    def get_top_students(self, n=3):
        sorted_students = sorted(self.students, key=lambda s: s.    average, reverse=True)
        return sorted_students[:n]

    def class_average(self):
        return sum(s.average for s in self.students) / len(self.    students)

    def failed_students(self):
        return list(filter(lambda s: get_grade(s.average) ==     "FAIL", self.students))


def main():
    parser = argparse.ArgumentParser(description="Student Grade Analyzer")
    parser.add_argument("--add", action="store_true", help="Add a new student")
    parser.add_argument("--report", action="store_true", help="Print class report")
    args = parser.parse_args()

    report = StudentReport()

    if args.add:
        name = input("Enter student name: ")
        scores = {}
        for subject in SUBJECTS:
            score = int(input(f"Enter score for {subject}: "))
            scores[subject] = score
        report.add_student(name, scores)
        print(f"\nStudent '{name}' added successfully!")

    if args.report:
        print("=" * 40)
        print("CLASS REPORT")
        print("=" * 40)

        if report.students:
          print(f"\nClass Average: {report.class_average():.1f}")
        else:
          print("\nNo students added yet.")

        print("\nTop 3 Students:")
        for student in report.get_top_students(3):
            print(f"  {student.name} — {student.average:.1f} ({get_grade(student.average)})")

        print("\nFailed Students:")
        failed = report.failed_students()
        if failed:
            for student in failed:
                print(f"  {student.name} — {student.average:.1f}")
        else:
            print("  None")

        print("\nIndividual Report Cards:")
        print("-" * 40)
        for student in report.students:
            print(student)
            print("-" * 40)


if __name__ == "__main__":
    main()