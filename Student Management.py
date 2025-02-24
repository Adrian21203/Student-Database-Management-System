import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import datetime


class FereastraPrincipala(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestionare Baza de Date Studenti")
        self.geometry("1000x700")

        # Titlu
        titlu = tk.Label(self, text="Studenti Management", font=("Serif", 24, "bold"))
        titlu.pack(pady=10)

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Panel pentru câmpurile text
        input_frame = tk.Frame(main_frame)
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        labels = ["ID Student", "Nume", "Prenume", "Adresa", "Cod Postal", "Telefon"]
        self.entries = {}

        for label_text in labels:
            label = tk.Label(input_frame, text=label_text, font=("Serif", 15, "bold"))
            label.pack(anchor=tk.W, pady=5)

            entry = tk.Entry(input_frame, font=("Serif", 13))
            entry.pack(fill=tk.X, pady=5)
            self.entries[label_text] = entry

        self.entries["Adresa"].bind("<FocusIn>", self.add_address_prefix)

        # Tabel
        table_frame = tk.Frame(main_frame)
        table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ["Id Student", "Nume", "Prenume", "Adresa", "CodPostal", "Telefon"]
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Butoane
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        buttons = [
            ("BD Connect", self.connect_db),
            ("Insert", self.insert),
            ("Reset", self.reset),
            ("Delete", self.delete),
            ("Update", self.update_data)
        ]

        for btn_text, btn_command in buttons:
            button = tk.Button(button_frame, text=btn_text, command=btn_command, font=("Serif", 15, "bold"), width=14)
            button.pack(side=tk.LEFT, padx=12, pady=6)

        self.conn = None
        self.cursor = None
        self.max_id = 0  

    def add_address_prefix(self, event):
        address_entry = self.entries["Adresa"]
        current_text = address_entry.get()
        if not current_text.startswith("Str. "):
            address_entry.delete(0, tk.END)
            address_entry.insert(0, "Str. " + current_text)

    def connect_db(self, show_message=True):
        try:
            self.conn = pyodbc.connect(
                r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                r'DBQ=C:\Users\win\OneDrive\Desktop\python\Studenti.accdb;'
            )
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT * FROM Studenti ORDER BY IdStudent")
            rows = self.cursor.fetchall()

            # Curăță tabelul înainte de a adăuga noi date
            self.tree.delete(*self.tree.get_children())  
            
            # Identifică cel mai mare ID
            self.max_id = 0
            for row in rows:
                formatted_row = tuple(str(item).strip("()").strip("'") for item in row)
                self.tree.insert("", tk.END, values=formatted_row)
                
                # Actualizează max_id
                current_id = int(formatted_row[0])  
                if current_id > self.max_id:
                    self.max_id = current_id

            # Setează câmpul ID Student la max_id + 1
            self.entries["ID Student"].delete(0, tk.END)
            self.entries["ID Student"].insert(0, str(self.max_id + 1))

            if show_message:
                messagebox.showinfo("Succes", "Conectare la baza de date reușită!")
        except pyodbc.Error as e:
            messagebox.showerror("Eroare", f"Eroare la conectarea la baza de date: {e}")

    
    def insert(self):
        try:
            # Verifică dacă toate câmpurile sunt completate
            for key, entry in self.entries.items():
                if not entry.get().strip():
                    raise ValueError("Toate câmpurile trebuie completate!")
                
            # Validare ID Student
            id_student = int(self.entries["ID Student"].get())
            if id_student != self.max_id + 1:
                raise ValueError(f"ID-ul trebuie să fie {self.max_id + 1}.")

            # Validare Cod Postal
            cod_postal = self.entries["Cod Postal"].get()
            if not cod_postal.isdigit() or len(cod_postal) != 6:
                raise ValueError("Codul postal trebuie să conțină exact 6 cifre!")

            # Validare Telefon
            telefon = self.entries["Telefon"].get()
            if not telefon.isdigit() or len(telefon) != 10:
                raise ValueError("Numărul de telefon trebuie să conțină exact 10 cifre!")

            # Validare Adresa
            adresa = self.entries["Adresa"].get()
            if not adresa.startswith("Str."):
                raise ValueError("Adresa trebuie să înceapă cu 'Str.'")

            nume = self.entries["Nume"].get()
            prenume = self.entries["Prenume"].get()

            query = """
            INSERT INTO Studenti (IdStudent, Nume, Prenume, Adresa, CodPostal, Telefon)
            VALUES(?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (id_student, nume, prenume, adresa, cod_postal, telefon))
            self.conn.commit()

            self.tree.insert("", tk.END, values=(id_student, nume, prenume, adresa, cod_postal, telefon))

            messagebox.showinfo("Succes", "Datele au fost inserate cu succes!")

            self.reset()

            # Reîncarcă datele și actualizează max_id
            self.connect_db(show_message=False)

        except ValueError as ve:
            messagebox.showerror("Eroare de validare", str(ve))
        except pyodbc.Error as e:
            messagebox.showerror("Eroare la inserare", f"Eroare la inserarea datelor: {e}")


    def reset(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def delete(self):
        try:
            # Obține ID-ul studentului de șters
            id_student = self.entries["ID Student"].get()
            
            # Verifică dacă ID-ul este valid și existent
            if not id_student.isdigit():
                raise ValueError("ID-ul trebuie să fie un număr.")
            
            id_student = int(id_student)
            
            # Verifică dacă ID-ul există în baza de date
            self.cursor.execute("SELECT 1 FROM Studenti WHERE IdStudent = ?", (id_student,))
            if not self.cursor.fetchone():
                raise ValueError("ID-ul studentului nu există în baza de date.")
            
            # Șterge studentul din baza de date
            self.cursor.execute("DELETE FROM Studenti WHERE IdStudent = ?", (id_student,))
            self.conn.commit()
            
            # Reordonează ID-urile după ștergere
            self.reorder_ids()

            # Resetează câmpurile
            self.reset()
            
            messagebox.showinfo("Succes", f"Studentul cu ID-ul {id_student} a fost șters cu succes!")

        except ValueError as ve:
            messagebox.showerror("Eroare de validare", str(ve))
        except pyodbc.Error as e:
            messagebox.showerror("Eroare la ștergere", f"Eroare la ștergerea datelor: {e}")

    def reorder_ids(self):
        try:
            # Obține toate înregistrările ordonate după ID
            self.cursor.execute("SELECT * FROM Studenti ORDER BY IdStudent")
            rows = self.cursor.fetchall()
            
            # Reasignează ID-urile în ordine secvențială
            new_id = 1
            for row in rows:
                current_id = row[0]  # Presupunem că primul câmp este ID-ul
                if current_id != new_id:
                    self.cursor.execute("UPDATE Studenti SET IdStudent = ? WHERE IdStudent = ?", (new_id, current_id))
                new_id += 1

            # Confirma modificările
            self.conn.commit()

            # Reîncarcă tabelul din interfață și actualizează max_id
            self.connect_db(show_message=False)

        except pyodbc.Error as e:
            messagebox.showerror("Eroare la reordonare", f"Eroare la reordonarea ID-urilor: {e}")


    def update_data(self):
        try:
            # Obține ID-ul studentului de actualizat
            id_student = self.entries["ID Student"].get().strip()
            
            # Verifică dacă ID-ul este valid
            if not id_student:
                raise ValueError("ID-ul nu poate fi gol.")
            if not id_student.isdigit():
                raise ValueError("ID-ul trebuie să fie un număr.")
            
            id_student = int(id_student)
            
            # Verifică dacă ID-ul există în baza de date
            self.cursor.execute("SELECT * FROM Studenti WHERE IdStudent = ?", (id_student))
            student_data = self.cursor.fetchone()
            if not student_data:
                raise ValueError("ID-ul studentului nu există în baza de date.")
            
            # Obține valorile actualizate din câmpurile de text
            nume = self.entries["Nume"].get().strip() or student_data[1]
            prenume = self.entries["Prenume"].get().strip() or student_data[2]
            adresa = self.entries["Adresa"].get().strip() or student_data[3]
            cod_postal = self.entries["Cod Postal"].get().strip() or student_data[4]
            telefon = self.entries["Telefon"].get().strip() or student_data[5]

            # Validări
            if cod_postal and (not cod_postal.isdigit() or len(cod_postal) != 6):
                raise ValueError("Codul postal trebuie să conțină exact 6 cifre!")

            if telefon and (not telefon.isdigit() or len(telefon) != 10):
                raise ValueError("Numărul de telefon trebuie să conțină exact 10 cifre!")
            
            if adresa and not adresa.startswith("Str."):
                raise ValueError("Adresa trebuie să înceapă cu 'Str.'")

            # Construiește interogarea SQL dinamică
            query = "UPDATE Studenti SET "
            parameters = []
            fields_to_update = []

            if nume != student_data[1]:
                fields_to_update.append("Nume = ?")
                parameters.append(nume)
            if prenume != student_data[2]:
                fields_to_update.append("Prenume = ?")
                parameters.append(prenume)
            if adresa != student_data[3]:
                fields_to_update.append("Adresa = ?")
                parameters.append(adresa)
            if cod_postal != student_data[4]:
                fields_to_update.append("CodPostal = ?")
                parameters.append(cod_postal)
            if telefon != student_data[5]:
                fields_to_update.append("Telefon = ?")
                parameters.append(telefon)

            if not fields_to_update:
                raise ValueError("Niciun câmp nu a fost selectat pentru actualizare.")

            query += ", ".join(fields_to_update) + " WHERE IdStudent = ?"
            parameters.append(id_student)

            # Execută interogarea
            self.cursor.execute(query, parameters)
            self.conn.commit()
            
            # Actualizează tabelul TreeView
            for item in self.tree.get_children():
                if self.tree.item(item, 'values')[0] == str(id_student):
                    self.tree.item(item, values=(
                        id_student,
                        nume,
                        prenume,
                        adresa,
                        cod_postal,
                        telefon
                    ))
                    break
            
            messagebox.showinfo("Succes", f"Datele studentului cu ID-ul {id_student} au fost actualizate cu succes!")
            self.reset()

        except ValueError as ve:
            messagebox.showerror("Eroare de validare", str(ve))
        except pyodbc.Error as e:
            messagebox.showerror("Eroare la actualizare", f"Eroare la actualizarea datelor: {e}")

if __name__ == "__main__":
    app = FereastraPrincipala()
    app.mainloop()
