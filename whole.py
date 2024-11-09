# Constants
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
EXAM_UNIT_USERNAME = "exam_unit"
EXAM_UNIT_PASSWORD = "exam123"
LECTURERS_FILE = "lecturers.txt"
EXAM_PAPERS_FILE = "exam_papers.txt"

# Initialize data structures
lecturers = {}
exam_papers = {
    "Set 1": {"Section A": [], "Section B": []},
    "Set 2": {"Section A": [], "Section B": []}
}

# Load data from files if they exist
def load_data():
    global lecturers, exam_papers
    try:
        with open(LECTURERS_FILE, 'r') as file:
            for line in file:
                username, password, profile = line.strip().split('|')
                # Convert profile string to dictionary
                profile_dict = {}
                for item in profile.strip('{}').split(','):
                    key, value = item.split(':')
                    profile_dict[key.strip().strip('"')] = value.strip().strip('"')
                lecturers[username] = {
                    "password": password,
                    "profile": profile_dict
                }
    except FileNotFoundError:
        pass  # No lecturers file found, continue with empty data

    try:
        with open(EXAM_PAPERS_FILE, 'r') as file:
            for line in file:
                set_name, sections = line.strip().split(':')
                # Convert sections string to dictionary
                sections_dict = {}
                for section in sections.split(','):
                    sec_name, questions = section.split('=')
                    sections_dict[sec_name.strip()] = questions.strip().split(';')
                exam_papers[set_name] = sections_dict
    except FileNotFoundError:
        pass  # No exam papers file found, continue with default data

# Save data to files
def save_data():
    with open(LECTURERS_FILE, 'w') as file:
        for username, data in lecturers.items():
            profile_str = ', '.join([f'"{key}": "{value}"' for key, value in data['profile'].items()])
            file.write(f"{username}|{data['password']}|{{{profile_str}}}\n")
    
    with open(EXAM_PAPERS_FILE, 'w') as file:
        for set_name, sections in exam_papers.items():
            sections_str = ', '.join([f"{sec}={'; '.join(questions)}" for sec, questions in sections.items()])
            file.write(f"{set_name}:{sections_str}\n")

# Function to validate date format
def validate_date(date_str):
    parts = date_str.split('.')
    if len(parts) != 3:
        return False
    day, month, year = parts
    if day.isdigit() and month.isdigit() and year.isdigit():
        if 1 <= int(day) <= 31 and 1 <= int(month) <= 12 and len(year) == 4:
            return True
    return False

# Function to validate password
def validate_password(password):
    if len(password) < 8:
        return False
    if any(char.isdigit() for char in password) or any(not char.isalnum() for char in password):
        return True
    return False

# Function for Admin Login
def admin_login():
    attempts = 3
    while attempts > 0:
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            print("Admin logged in successfully.")
            return True
        else:
            attempts -= 1
            print(f"Incorrect credentials. Attempts left: {attempts}")
    print("Too many failed attempts. Exiting...")
    return False

# Function to Assign New Lecturer
def assign_lecturer():
    username = input("Enter new lecturer username: ")
    while True:
        password = input("Enter new lecturer password (at least 8 characters, with a number or special character): ")
        if validate_password(password):
            break
        else:
            print("Password must be at least 8 characters long and contain at least one number or special character.")
    lecturers[username] = {"password": password, "profile": {}}
    save_data()  # Save after assigning a lecturer
    print(f"Lecturer {username} assigned successfully.")

# Function to Add Lecturer Profile
def add_lecturer_profile():
    username = input("Enter lecturer username to add profile: ")
    if username in lecturers:
        profile = {
            "name": input("Enter name: "),
            "address": input("Enter address: "),
            "contact": input("Enter contact number: ")
        }
        lecturers[username]["profile"] = profile
        save_data()  # Save after adding profile
        print("Profile added successfully.")
    else:
        print("Lecturer not found.")

# Function to Modify Lecturer Profile
def modify_lecturer_profile():
    username = input("Enter lecturer username to modify profile: ")
    if username in lecturers:
        profile = lecturers[username]["profile"]
        if profile:
            while True:
                dob = input("Enter date of birth (dd.mm.yyyy): ")
                if validate_date(dob):
                    profile["dob"] = dob
                    break
                else:
                    print("Invalid date format. Please enter in dd.mm.yyyy format.")
            profile["email"] = input("Enter email address: ")
            profile["age"] = input("Enter age: ")
            profile["citizenship"] = input("Enter citizenship: ")
            profile["contact"] = input("Enter contact number: ")
            save_data()  # Save after modifying profile
            print("Profile updated successfully.")
        else:
            print("No profile found for this lecturer.")
    else:
        print("Lecturer not found.")

# Function to Delete Lecturer
def delete_lecturer():
    username = input("Enter lecturer username to delete: ")
    if username in lecturers:
        del lecturers[username]
        save_data()  # Save after deleting a lecturer
        print("Lecturer deleted successfully.")
    else:
        print("Lecturer not found.")

# Function for Lecturer Login
def lecturer_login():
    attempts = 3
    while attempts > 0:
        username = input("Enter lecturer username: ")
        password = input("Enter lecturer password: ")
        if username in lecturers and lecturers[username]["password"] == password:
            print("Lecturer logged in successfully.")
            return username
        else:
            attempts -= 1
            print(f"Incorrect credentials. Attempts left: {attempts}")
    print("Too many failed attempts. Exiting...")
    return None

# Function to Change Lecturer Username and Password
def change_lecturer_credentials(username):
    new_username = input("Enter new username: ")
    while True:
        new_password = input("Enter new password (at least 8 characters, with a number or special character): ")
        if validate_password(new_password):
            break
        else:
            print("Password must be at least 8 characters long and contain at least one number or special character.")
    lecturers[new_username] = lecturers.pop(username)
    lecturers[new_username]["password"] = new_password
    save_data()  # Save after changing credentials
    print("Updated information successfully.")

# Function to Add Questions
def add_questions(username):
    questions = []
    num_questions = int(input("How many questions do you want to add? "))
    for _ in range(num_questions):
        question = input("Enter question: ")
        answer = input("Enter answer: ")
        questions.append({"question": question, "answer": answer})
    print("Questions added successfully.")
    return questions

# Function to Modify Questions
def modify_questions(questions):
    for idx, q in enumerate(questions):
        print(f"{idx + 1}: {q['question']}")
    question_index = int(input("Enter question number to modify: ")) - 1
    if 0 <= question_index < len(questions):
        questions[question_index]["question"] = input("Enter new question: ")
        questions[question_index]["answer"] = input("Enter new answer: ")
        print("Question modified successfully.")
    else:
        print("Invalid question number.")

# Function to View Questions
def view_questions(questions):
    for q in questions:
        print(f"Q: {q['question']} | A: {q['answer']}")

# Function for Exam Unit Personnel Login
def exam_unit_login():
    attempts = 3
    while attempts > 0:
        username = input("Enter exam unit username: ")
        password = input("Enter exam unit password: ")
        if username == EXAM_UNIT_USERNAME and password == EXAM_UNIT_PASSWORD:
            print("Exam unit personnel logged in successfully.")
            return True
        else:
            attempts -= 1
            print(f"Incorrect credentials. Attempts left: {attempts}")
    print("Too many failed attempts. Exiting...")
    return False

# Function to Create Exam Papers
def create_exam_paper():
    set_name = input("Enter the name of the exam set: ")
    if set_name not in exam_papers:
        exam_papers[set_name] = {}
    
    while True:
        section_name = input("Enter section name (or type 'done' to finish): ")
        if section_name.lower() == 'done':
            break
        
        num_questions = int(input(f"How many questions for {section_name}? "))
        questions = []
        for _ in range(num_questions):
            question = input("Enter question: ")
            questions.append(question)
        
        exam_papers[set_name][section_name] = questions
    
    save_data()  # Save after creating exam papers
    print(f"Exam paper '{set_name}' created successfully!")

# Function to View Exam Papers
def view_exam_papers():
    for set_name, sections in exam_papers.items():
        print(f"{set_name}:")
        for section, questions in sections.items():
            print(f"  {section}: {questions}")

# Main Function to Run the Application
def main():
    load_data()  # Load data at the start of the program
    while True:
        print(" <<<<<<<<<Welcome to the TMS>>>>>>>>>>>")
        print("\n1. Admin Division \n2. Lecturer Division \n3. Exam Unit Division \n4. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            if admin_login():
                while True:
                    print("\nAdmin Menu:")
                    print("1. Assign Lecturer")
                    print("2. Add Lecturer Profile")
                    print("3. Modify Lecturer Profile")
                    print("4. Delete Lecturer")
                    print("5. Exit")
                    admin_choice = input("Select an option: ")
                    if admin_choice == '1':
                        assign_lecturer()
                    elif admin_choice == '2':
                        add_lecturer_profile()
                    elif admin_choice == '3':
                        modify_lecturer_profile()
                    elif admin_choice == '4':
                        delete_lecturer()
                    elif admin_choice == '5':
                        break

        elif choice == '2':
            username = lecturer_login()
            if username:
                questions = []
                while True:
                    print("\nLecturer Menu:")
                    print("1. Change Credentials")
                    print("2. Add Questions")
                    print("3. Modify Questions")
                    print("4. View Questions")
                    print("5. Exit")
                    lecturer_choice = input("Select an option: ")
                    if lecturer_choice == '1':
                        change_lecturer_credentials(username)
                    elif lecturer_choice == '2':
                        questions.extend(add_questions(username))
                    elif lecturer_choice == '3':
                        modify_questions(questions)
                    elif lecturer_choice == '4':
                        view_questions(questions)
                    elif lecturer_choice == '5':
                        break

        elif choice == '3':
            if exam_unit_login():
                while True:
                    print("\nExam Unit Menu:")
                    print("1. Create Exam Papers")
                    print("2. View Exam Papers")
                    print("3. Exit")
                    exam_unit_choice = input("Select an option: ")
                    if exam_unit_choice == '1':
                        create_exam_paper()
                    elif exam_unit_choice == '2':
                        view_exam_papers()
                    elif exam_unit_choice == '3':
                        break

        elif choice == '4':
            print("Exiting the application. Goodbye!")
            break

if __name__ == "__main__":
    main()
