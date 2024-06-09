import tkinter
import customtkinter
from tkinter import messagebox
from tkinter import ttk
import main2
class log:
    def up():
# Set appearance mode and default color theme
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("green")

        # Path to the file storing user credentials
        USER_FILE = 'users.txt'

        def read_users_from_file():
            users = {}
            try:
                with open(USER_FILE, 'r') as file:
                    for line in file:
                        user_id, password = line.strip().split(',')
                        users[user_id] = password
            except FileNotFoundError:
                pass
            return users

        def write_user_to_file(user_id, password):
            with open(USER_FILE, 'a') as file:
                file.write(f'{user_id},{password}\n')

        # Function to handle the sign-up screen
        def sign_up_screen(initial_id="", initial_password=""):
            sign_up_app = customtkinter.CTk()  # Create the new window
            sign_up_app.geometry("600x600")  # Increase window height to accommodate more fields
            sign_up_app.title('Sign Up')

            def submit_sign_up():
                # Retrieve values from entry fields
                new_id = entry_new_id.get()
                new_password = entry_new_password.get()
                confirm_password = entry_confirm_password.get()
                name = entry_name.get()
                age = entry_age.get()
                gender = entry_gender.get()
                problems = entry_problems.get()
                phone_no = entry_phone_no.get()

                # Validate fields
                users = read_users_from_file()
                if new_id in users:
                    messagebox.showerror("Error", "ID already exists")
                    return
                if new_password != confirm_password:
                    messagebox.showerror("Error", "Passwords do not match")
                    return

                # Write user data to file (you can adjust this as needed)
                write_user_to_file(new_id, new_password)

                # Show success message
                messagebox.showinfo("Sign Up", "Sign-up successful!")

                # Destroy sign-up window and show welcome screen or perform other actions
                sign_up_app.destroy()
                main2.Home.page()

            # Sign-up form
            frame = customtkinter.CTkFrame(master=sign_up_app, width=400, height=500, corner_radius=15)
            frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            l1 = customtkinter.CTkLabel(master=frame, text="Create a New Account", font=('Century Gothic', 20))
            l1.place(relx=0.5, rely=0.05, anchor=tkinter.CENTER)

            entry_new_id = customtkinter.CTkEntry(master=frame, width=300, placeholder_text='ID')
            entry_new_id.place(relx=0.5, rely=0.12, anchor=tkinter.CENTER)

            entry_new_password = customtkinter.CTkEntry(master=frame, width=300, placeholder_text='Password', show="*")
            entry_new_password.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

            entry_confirm_password = customtkinter.CTkEntry(master=frame, width=300, placeholder_text='Confirm Password', show="*")
            entry_confirm_password.place(relx=0.5, rely=0.28, anchor=tkinter.CENTER)

            entry_name = customtkinter.CTkEntry(master=frame, width=300, placeholder_text='Name')
            entry_name.place(relx=0.5, rely=0.36, anchor=tkinter.CENTER)

            entry_age = customtkinter.CTkEntry(master=frame, width=300, placeholder_text='Age')
            entry_age.place(relx=0.5, rely=0.44, anchor=tkinter.CENTER)

            entry_gender = customtkinter.CTkEntry(master=frame, width=300, placeholder_text='Gender')
            entry_gender.place(relx=0.5, rely=0.52, anchor=tkinter.CENTER)

            entry_problems = customtkinter.CTkEntry(master=frame, width=300, placeholder_text='Problems')
            entry_problems.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

            entry_phone_no = customtkinter.CTkEntry(master=frame, width=300, placeholder_text='Phone Number')
            entry_phone_no.place(relx=0.5, rely=0.68, anchor=tkinter.CENTER)

            button_submit = customtkinter.CTkButton(master=frame, width=220, text="Sign Up", command=submit_sign_up, corner_radius=6)
            button_submit.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

            # Dark mode switch
            def changemode():
                val = switch.get()
                if val:
                    customtkinter.set_appearance_mode("dark")
                else:
                    customtkinter.set_appearance_mode("light")

            switch = customtkinter.CTkSwitch(master=sign_up_app, text="Dark Mode",
                           onvalue=1,
                           offvalue=0,
                           command=changemode)

            switch.place(relx=0.95, rely=0.05, anchor=tkinter.NE)  # Place at the top right corner

            sign_up_app.mainloop()

        # Function to handle the welcome screen after login
        def welcome_screen(user_id):
            # Example welcome screen
            welcome_app = customtkinter.CTk()
            welcome_app.geometry("400x300")
            welcome_app.title('Welcome')

            label_welcome = customtkinter.CTkLabel(master=welcome_app, text=f"Welcome {user_id}!", font=('Century Gothic', 20))
            label_welcome.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            welcome_app.mainloop()

        # Function to handle login button click
        def login():
            user_id = entry_id.get()
            password = entry_password.get()
            users = read_users_from_file()

            if user_id in users and users[user_id] == password:
                messagebox.showinfo("Login", "Login successful!")
                app.destroy()
                main2.Home()
            else:
                messagebox.showinfo("Login", "ID does not exist, redirecting to sign-up page...")
                app.destroy()
                sign_up_screen(user_id, password)

        # Function to show the sign-up screen
        def show_sign_up_screen():
            app.destroy()  # Destroy the login screen
            sign_up_screen()

        # Initialize the main application window
        app = customtkinter.CTk()
        app.geometry("600x400")
        app.title('Login')

        # Create a frame for the login form
        frame = customtkinter.CTkFrame(master=app, width=400, height=300, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # Label for the login form
        l2 = customtkinter.CTkLabel(master=frame, text="Log into your Account", font=('Century Gothic', 20))
        l2.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

        # ID entry field
        entry_id = customtkinter.CTkEntry(master=frame, width=300, placeholder_text='ID')
        entry_id.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        # Password entry field
        entry_password = customtkinter.CTkEntry(master=frame, width=300, placeholder_text='Password', show="*")
        entry_password.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        # Login button
        button1 = customtkinter.CTkButton(master=frame, width=220, text="Login", command=login, corner_radius=6)
        button1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # Sign up button
        button_sign_up = customtkinter.CTkButton(master=frame, width=220, text="Sign Up", command=show_sign_up_screen, corner_radius=6)
        button_sign_up.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        # Dark mode switch
        def changemode():
            val = switch.get()
            if val:
                customtkinter.set_appearance_mode("dark")
            else:
                customtkinter.set_appearance_mode("light")

        switch = customtkinter.CTkSwitch(master=app, text="Dark Mode",
                       onvalue=1,
                       offvalue=0,
                       command=changemode)

        switch.place(relx=0.95, rely=0.05, anchor=tkinter.NE)  # Place at the top right corner

        # Start the main loop of the application
        app.mainloop()
if __name__ == "__main__":
    log.up()