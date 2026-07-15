import csv

FIELDS = ["RollNo", "FullName", "Age", "Email", "Phone"]
DATABASE_FILE = "students.csv"


def show_menu():
    print("\n==============================")
    print("   Student Management Portal   ")
    print("==============================")
    print("1. Register New Student")
    print("2. Display All Students")
    print("3. Find Student")
    print("4. Modify Student")
    print("5. Remove Student")
    print("6. Exit")
    print("==============================\n")


def register_student():
    print("\n--- Register New Student ---")
    student_info = {}
    for field in FIELDS:
        student_info[field] = input(f"Enter {field}: ")

    with open(DATABASE_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(student_info)

    print("✅ Student registered successfully!")


def display_students():
    print("\n--- Student Records ---")
    try:
        with open(DATABASE_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            students = list(reader)

            if not students:
                print("⚠️ No student data found.")
                return

            for student in students:
                print(" | ".join([f"{k}: {v}" for k, v in student.items()]))

    except FileNotFoundError:
        print("⚠️ No records found. Please register a student first.")


def find_student():
    roll = input("Enter Roll Number to search: ")
    found = False

    try:
        with open(DATABASE_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for student in reader:
                if student["RollNo"] == roll:
                    print("\n✅ Student Found:")
                    for key, value in student.items():
                        print(f"{key}: {value}")
                    found = True
                    break
    except FileNotFoundError:
        pass

    if not found:
        print("❌ Student not found.")


def modify_student():
    roll = input("Enter Roll Number to update: ")
    updated_records = []
    modified = False

    try:
        with open(DATABASE_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for student in reader:
                if student["RollNo"] == roll:
                    print("Enter new details (leave blank to keep existing):")
                    for field in FIELDS:
                        new_value = input(f"{field} ({student[field]}): ")
                        if new_value.strip():
                            student[field] = new_value
                    modified = True
                updated_records.append(student)

        if modified:
            with open(DATABASE_FILE, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(updated_records)
            print("✅ Student details updated successfully!")
        else:
            print("❌ Student not found.")

    except FileNotFoundError:
        print("⚠️ No data available to update.")


def remove_student():
    roll = input("Enter Roll Number to delete: ")
    updated_records = []
    deleted = False

    try:
        with open(DATABASE_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for student in reader:
                if student["RollNo"] != roll:
                    updated_records.append(student)
                else:
                    deleted = True

        if deleted:
            with open(DATABASE_FILE, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(updated_records)
            print(f"✅ Student with Roll No. {roll} deleted successfully.")
        else:
            print("❌ Student not found.")

    except FileNotFoundError:
        print("⚠️ No data available to delete.")


if __name__ == "__main__":
    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            register_student()
        elif choice == "2":
            display_students()
        elif choice == "3":
            find_student()
        elif choice == "4":
            modify_student()
        elif choice == "5":
            remove_student()
        elif choice == "6":
            print("\n👋 Thank you for using the Student Management Portal. Goodbye!")
            break
        else:
            print("⚠️ Invalid choice, please try again.")
