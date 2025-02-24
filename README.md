# Student Database Management System

This is a Python-based application that provides a Graphical User Interface (GUI) for managing a Microsoft Access database containing student records. The app allows users to perform CRUD (Create, Read, Update, Delete) operations on the database.

## Features

1. **Database Connection**
   - The application connects to a local Microsoft Access database.
   - Once connected, it fetches and displays all records from the `Studenti` table, ordered by Student ID.

2. **Add New Student**
   - Users can add new student records by entering:
     - **Student ID:** Automatically assigned based on the highest existing ID.
     - **First Name**
     - **Last Name**
     - **Address:** Must start with "Str.".
     - **Postal Code:** Must be exactly 6 digits.
     - **Phone Number:** Must be exactly 10 digits.
   - The app validates the input and inserts the data into the database if valid.

3. **Delete Student**
   - Users can delete a student by entering the Student ID.
   - The app ensures that the ID exists in the database before deleting the record.

4. **Update Student Information**
   - Users can update student records, including:
     - **First Name**
     - **Last Name**
     - **Address**
     - **Postal Code**
     - **Phone Number**
   - The app checks if the ID exists and ensures the data is valid before updating the record.

5. **View Student Records**
   - All student records are displayed in a table with columns for:
     - **Student ID**
     - **First Name**
     - **Last Name**
     - **Address**
     - **Postal Code**
     - **Phone Number**
   - The table automatically updates when records are added, updated, or deleted.

6. **Reset Form**
   - After performing any operations, the input fields are cleared, allowing the user to add a new student or perform another operation.

## Technologies Used

- **Tkinter:** For creating the graphical user interface (GUI).
- **PyODBC:** For connecting to and interacting with the Microsoft Access database.
- **Microsoft Access Database:** The backend database used to store student records.

## Installation Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/student-database-management.git
   cd student-database-management

2. **Install required dependencies:**
   -Ensure that you have Python 3.x installed on your system. You can install the required dependencies using pip:

   ```bash
   pip install pyodbc

3. **Database Configuration:**
   - The database file (`Studenti.accdb`) should be available at a specific location. By default, the code assumes the database is located at:

   ```plaintext
   C:\Users\win\OneDrive\Desktop\python\Studenti.accdb


4. **Run the application:**
   - After setting up the database, you can run the application with the following command:

   ```bash
   python app.py


## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

The MIT License is a permissive free software license, meaning you can freely use, modify, and distribute this code, as long as you include the original license notice in all copies or substantial portions of the software. 

### Key Points:
- You can use the software for personal or commercial purposes.
- You can modify the software as needed.
- The software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement.

