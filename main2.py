import tkinter as tk
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import threading
import time
import main3
import hackprix1
import main

class Home:
    def __init__(self):
        self.entries = {}
        self.total_carbs = 0
        self.total_protein = 0
        self.total_fats = 0
        self.medicines = []
        self.lock = threading.Lock()

        self.app = ctk.CTk()
        self.app.geometry("995x600")
        self.app.title('Macronutrient Tracker & Medicine Reminder')

        self.create_menu()
        self.create_frames()
        self.create_widgets()

        self.canvas = None
        self.update_pie_chart()

        self.reminder_thread = threading.Thread(target=self.check_reminders, daemon=True)
        self.reminder_thread.start()

        self.app.mainloop()

    def create_menu(self):
        menu = tk.Menu(self.app)
        self.app.configure(menu=menu)

        dropdown_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Menu", menu=dropdown_menu)
        dropdown_menu.add_command(label="Diagnosis", command=hackprix1.DiseaseDiagnosisApp.don, font=('Arial', 23))
        dropdown_menu.add_command(label="Logout", command=self.doi, font=('Arial', 23))

    def rem(self):
        if self.canvas:
            try:
                self.canvas.get_tk_widget().destroy()
            except Exception as e:
                print(f"Error destroying canvas: {e}")
        main3.Shop.do()

    def create_frames(self):
        self.frame_main = ctk.CTkFrame(master=self.app, width=800, height=400, corner_radius=15)
        self.frame_main.pack(side=tk.LEFT, anchor="nw")

        self.frame_chart = ctk.CTkFrame(master=self.frame_main, width=400, height=400, corner_radius=15)
        self.frame_chart.pack(side=tk.LEFT)

        self.frame_reminders = ctk.CTkFrame(master=self.frame_main, width=400, height=400, corner_radius=15)
        self.frame_reminders.pack(side=tk.RIGHT)

        self.frame_entry = ctk.CTkFrame(master=self.app, width=800, height=600, corner_radius=15)
        self.frame_medicine_entry = ctk.CTkFrame(master=self.app, width=800, height=600, corner_radius=15)

    def create_widgets(self):
        button_add_entry = ctk.CTkButton(master=self.frame_main, text="Add Entry", command=self.switch_to_entry_page)
        button_add_entry.pack(pady=20)

        button_add_medicine_page = ctk.CTkButton(master=self.frame_main, text="Add Medicine Reminder", command=self.switch_to_medicine_entry_page)
        button_add_medicine_page.pack(pady=20)

        ctk.CTkLabel(master=self.frame_entry, text="Food Name:", font=('Century Gothic', 16)).pack(pady=5)
        self.entry_food_name = ctk.CTkEntry(master=self.frame_entry, width=200)
        self.entry_food_name.pack(pady=5)

        ctk.CTkLabel(master=self.frame_entry, text="Carbs (g):", font=('Century Gothic', 16)).pack(pady=5)
        self.entry_carbs = ctk.CTkEntry(master=self.frame_entry, width=200)
        self.entry_carbs.pack(pady=5)

        ctk.CTkLabel(master=self.frame_entry, text="Protein (g):", font=('Century Gothic', 16)).pack(pady=5)
        self.entry_protein = ctk.CTkEntry(master=self.frame_entry, width=200)
        self.entry_protein.pack(pady=5)

        ctk.CTkLabel(master=self.frame_entry, text="Fats (g):", font=('Century Gothic', 16)).pack(pady=5)
        self.entry_fats = ctk.CTkEntry(master=self.frame_entry, width=200)
        self.entry_fats.pack(pady=5)

        button_calculate = ctk.CTkButton(master=self.frame_entry, text="Add", command=self.calculate_macronutrients)
        button_calculate.pack(pady=20)
        button_return = ctk.CTkButton(master=self.frame_entry, text="Back", command=self.macro_to_main)
        button_return.pack(pady=20)

        self.error_label = ctk.CTkLabel(master=self.frame_entry, text="", font=('Century Gothic', 16), text_color="red")

        frame_medicine_inputs = ctk.CTkFrame(master=self.frame_medicine_entry, width=400, height=400, corner_radius=15)
        frame_medicine_inputs.pack(side=tk.TOP, pady=20)

        ctk.CTkLabel(master=frame_medicine_inputs, text="Medicine Name:", font=('Century Gothic', 16)).pack(pady=5)
        self.entry_medicine_name = ctk.CTkEntry(master=frame_medicine_inputs, width=200)
        self.entry_medicine_name.pack(pady=5)

        ctk.CTkLabel(master=frame_medicine_inputs, text="Dosage:", font=('Century Gothic', 16)).pack(pady=5)
        self.entry_dosage = ctk.CTkEntry(master=frame_medicine_inputs, width=200)
        self.entry_dosage.pack(pady=5)

        ctk.CTkLabel(master=frame_medicine_inputs, text="Reminder Time (HH:MM):", font=('Century Gothic', 16)).pack(pady=5)
        self.entry_time = ctk.CTkEntry(master=frame_medicine_inputs, width=200)
        self.entry_time.pack(pady=5)

        button_add_medicine = ctk.CTkButton(master=frame_medicine_inputs, text="Add Reminder", command=self.add_medicine_reminder)
        button_add_medicine.pack(pady=20)

        self.medicine_error_label = ctk.CTkLabel(master=frame_medicine_inputs, text="", font=('Century Gothic', 16), text_color="red")

        button_back_to_main = ctk.CTkButton(master=self.frame_medicine_entry, text="Back", command=self.switch_to_main_from_medicine_entry)
        button_back_to_main.pack(pady=20)

    def calculate_macronutrients(self):
        try:
            food_name = self.entry_food_name.get().strip()
            carbs = float(self.entry_carbs.get().strip())
            protein = float(self.entry_protein.get().strip())
            fats = float(self.entry_fats.get().strip())

            if not food_name:
                raise ValueError("Food name cannot be empty.")
            if carbs < 0 or protein < 0 or fats < 0:
                raise ValueError("Macronutrient values cannot be negative.")
            total = carbs + protein + fats
            if total == 0:
                raise ValueError("Total intake cannot be zero.")

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.entries[timestamp] = {'food_name': food_name, 'carbs': carbs, 'protein': protein, 'fats': fats}

            self.total_carbs += carbs
            self.total_protein += protein
            self.total_fats += fats

            self.clear_entries()
            self.update_pie_chart()
            self.switch_to_main_page()

        except ValueError as e:
            self.display_error_message(str(e))

    def display_error_message(self, message):
        self.error_label.configure(text=message)
        self.error_label.pack()

    def update_pie_chart(self):
        try:
            fig, ax = plt.subplots()
            if self.total_carbs + self.total_protein + self.total_fats == 0:
                ax.pie([1], labels=[''], colors=['lightgray'], autopct='%1.1f%%', startangle=140)
            else:
                carbs_percentage = (self.total_carbs / (self.total_carbs + self.total_protein + self.total_fats)) * 100
                protein_percentage = (self.total_protein / (self.total_carbs + self.total_protein + self.total_fats)) * 100
                fats_percentage = (self.total_fats / (self.total_carbs + self.total_protein + self.total_fats)) * 100

                labels = 'Carbs', 'Protein', 'Fats'
                sizes = [carbs_percentage, protein_percentage, fats_percentage]
                colors = ['#ff9999', '#66b3ff', '#99ff99']
                explode = (0.1, 0, 0)

                ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
            ax.axis('equal')

            if self.canvas:
                self.canvas.get_tk_widget().destroy()

            self.canvas = FigureCanvasTkAgg(fig, master=self.frame_chart)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack()
        except Exception as e:
            print(f"Error updating pie chart: {e}")

    def clear_entries(self):
        self.entry_food_name.delete(0, tk.END)
        self.entry_carbs.delete(0, tk.END)
        self.entry_protein.delete(0, tk.END)
        self.entry_fats.delete(0, tk.END)
        self.error_label.pack_forget()

    def switch_to_entry_page(self):
        self.frame_main.pack_forget()
        self.frame_entry.pack(side=tk.LEFT, anchor="nw")

    def switch_to_main_page(self):
        self.frame_entry.pack_forget()
        self.frame_main.pack(side=tk.LEFT, anchor="nw")

    def switch_to_medicine_entry_page(self):
        self.frame_main.pack_forget()
        self.frame_medicine_entry.pack(side=tk.LEFT, anchor="nw")

    def switch_to_main_from_medicine_entry(self):
        self.frame_medicine_entry.pack_forget()
        self.frame_main.pack(side=tk.LEFT, anchor="nw")

    def macro_to_main(self):
        self.frame_entry.pack_forget()
        self.frame_main.pack(side=tk.LEFT, anchor="nw")

    def add_medicine_reminder(self):
        try:
            medicine_name = self.entry_medicine_name.get().strip()
            dosage = self.entry_dosage.get().strip()
            reminder_time = self.entry_time.get().strip()

            if not medicine_name or not dosage or not reminder_time:
                raise ValueError("All fields must be filled out.")

            reminder_datetime = datetime.strptime(reminder_time, "%H:%M")
            reminder_datetime = datetime.combine(datetime.today(), reminder_datetime.time())
            if reminder_datetime < datetime.now():
                reminder_datetime += timedelta(days=1)

            with self.lock:
                self.medicines.append({
                    "name": medicine_name,
                    "dosage": dosage,
                    "time": reminder_datetime
                })

            self.update_medicine_reminders()
            self.clear_medicine_entries()
            self.switch_to_main_from_medicine_entry()

        except ValueError as e:
            self.display_medicine_error_message(str(e))

    def display_medicine_error_message(self, message):
        self.medicine_error_label.configure(text=message)
        self.medicine_error_label.pack()

    def clear_medicine_entries(self):
        self.entry_medicine_name.delete(0, tk.END)
        self.entry_dosage.delete(0, tk.END)
        self.entry_time.delete(0, tk.END)
        self.medicine_error_label.pack_forget()

    def update_medicine_reminders(self):
        for widget in self.frame_reminders.winfo_children():
            widget.destroy()

        if self.medicines:
            with self.lock:
                sorted_medicines = sorted(self.medicines, key=lambda x: x["time"])
            for med in sorted_medicines:
                reminder_label = ctk.CTkLabel(master=self.frame_reminders, text=f"{med['name']} - {med['dosage']} at {med['time'].strftime('%H:%M')}")
                reminder_label.pack(pady=5)
        else:
            no_reminder_label = ctk.CTkLabel(master=self.frame_reminders, text="No reminders set.")
            no_reminder_label.pack(pady=5)

    def check_reminders(self):
        while True:
            current_time = datetime.now()
            with self.lock:
                for med in list(self.medicines):
                    if med["time"] <= current_time:
                        self.display_alert(f"Time to take your medicine: {med['name']} - {med['dosage']}")
                        self.medicines.remove(med)
                        self.update_medicine_reminders()
            time.sleep(60)

    def display_alert(self, message):
        alert_window = ctk.CTkToplevel()
        alert_window.geometry("300x150")
        alert_window.title("Reminder")
        alert_label = ctk.CTkLabel(master=alert_window, text=message, font=('Century Gothic', 16))
        alert_label.pack(pady=20)
        alert_button = ctk.CTkButton(master=alert_window, text="OK", command=alert_window.destroy)
        alert_button.pack(pady=20)

    def doi(self):
        self.app.destroy()
        main.log.up()

if __name__ == "__main__":
    Home()
