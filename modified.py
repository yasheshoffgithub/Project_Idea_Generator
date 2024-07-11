import os
import google.generativeai as genai
import customtkinter as ctk
from dotenv import load_dotenv
import re
from tkinter import messagebox, filedialog, Toplevel, Label, Entry, Button
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load API key from .env file
load_dotenv()
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def generate():
    try:
        prompt = "Please generate 10 ideas for coding projects."
        language = lang_dropdown.get()
        prompt += " The Programming language is " + language + ". "
        difficulty = diff_value.get()
        prompt += " The difficulty is " + difficulty + ". "
        if check1.get():
            prompt += " The project should include a database."
        if check2.get():
            prompt += " The project should include an API."

        model = genai.GenerativeModel('gemini-1.0-pro-latest')
        response = model.generate_content(prompt)

        # Formatting the response
        formatted_text = re.sub(r'\*\*(.*?)\*\*', r'\1', response.text)
        
        result.delete("1.0", ctk.END)  # Clear previous results
        result.insert("1.0", formatted_text)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def save_to_file():
    try:
        text_to_save = result.get("1.0", ctk.END)
        if text_to_save.strip():
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(text_to_save)
                messagebox.showinfo("Success", "File saved successfully!")
            else:
                messagebox.showwarning("Warning", "Save operation cancelled.")
        else:
            messagebox.showwarning("Warning", "There is no text to save.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving the file: {e}")

def clear_ideas():
    result.delete("1.0", ctk.END)

def open_feedback():
    feedback_window = Toplevel(root)
    feedback_window.title("Feedback")
    feedback_window.geometry("400x300")
    
    Label(feedback_window, text="Name/Email:").pack(pady=10)
    name_entry = Entry(feedback_window, width=40)
    name_entry.pack(pady=5)
    
    Label(feedback_window, text="Feedback:").pack(pady=10)
    feedback_entry = Entry(feedback_window, width=40)
    feedback_entry.pack(pady=5)
    
    def submit_feedback():
        name = name_entry.get()
        feedback = feedback_entry.get()
        if name and feedback:
            save_feedback(name, feedback)
            feedback_window.destroy()
            messagebox.showinfo("Feedback Received", "Thank you for your feedback!")
        else:
            messagebox.showwarning("Input Error", "Please provide both name/email and feedback.")
    
    Button(feedback_window, text="Submit", command=submit_feedback).pack(pady=20)

def save_feedback(name, feedback):
    feedback_data = {'Name/Email': [name], 'Feedback': [feedback]}
    feedback_df = pd.DataFrame(feedback_data)
    
    if os.path.exists("feedback.xlsx"):
        existing_df = pd.read_excel("feedback.xlsx")
        feedback_df = pd.concat([existing_df, feedback_df], ignore_index=True)
    
    feedback_df.to_excel("feedback.xlsx", index=False)

def open_email_window():
    email_window = Toplevel(root)
    email_window.geometry("400x200")
    email_window.title("Share via Email")

    Label(email_window, text="Recipient's Email:").pack(pady=10)
    email_entry = Entry(email_window, width=40)
    email_entry.pack(pady=5)

    def send_email():
        recipient_email = email_entry.get()
        if recipient_email:
            try:
                sender_email = "yps123vasu@gmail.com"  # Replace with your Gmail address
                sender_password = "rvax bwtu kdws gtwd"        # Replace with your Gmail app password

                # Email content
                subject = "Shared Project Ideas"
                body = result.get("1.0", ctk.END)

                # Setting up the MIME
                message = MIMEMultipart()
                message['From'] = sender_email
                message['To'] = recipient_email
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))

                # Sending the email
                server = smtplib.SMTP('smtp.gmail.com', 587)  # SMTP server for Gmail
                server.starttls()
                server.login(sender_email, sender_password)
                text = message.as_string()
                server.sendmail(sender_email, recipient_email, text)
                server.quit()

                messagebox.showinfo("Success", "Email sent successfully!")
                email_window.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to send email: {e}")
                email_window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please enter a recipient email address.")
    
    Button(email_window, text="Send", command=send_email).pack(pady=20)

# Setting up the main window
root = ctk.CTk()
root.title("Gemini Project Idea Generator")

ctk.set_appearance_mode("dark")

# Title Label
title_label = ctk.CTkLabel(root, text="Project Idea Generator", font=ctk.CTkFont(size=30, weight="bold"))
title_label.pack(padx=10, pady=(40,20))

frame = ctk.CTkFrame(root)
frame.pack(fill="x", padx=100)

# Language Frame
language_frame = ctk.CTkFrame(frame)
language_frame.pack(padx=100, pady=(20,5), fill="both")
language_label = ctk.CTkLabel(language_frame, text="Programming Language", font=ctk.CTkFont(weight="bold"))
language_label.pack()

lang_dropdown = ctk.CTkComboBox(language_frame, values=["Python", "Java", "C++", "Javascript", "Golang"])
lang_dropdown.pack(pady=10)

# Difficulty Frame
diff_frame = ctk.CTkFrame(frame)
diff_frame.pack(padx=100, pady=5, fill="both")

difficulty_label = ctk.CTkLabel(diff_frame, text="Project Difficulty", font=ctk.CTkFont(weight="bold"))
difficulty_label.grid(row=0, column=0, columnspan=3, pady=10)

diff_value = ctk.StringVar(value="Easy")
radio1 = ctk.CTkRadioButton(diff_frame, text="Easy", variable=diff_value, value="Easy")
radio1.grid(row=1, column=0, padx=10, pady=10)

radio2 = ctk.CTkRadioButton(diff_frame, text="Medium", variable=diff_value, value="Medium")
radio2.grid(row=1, column=1, padx=10, pady=10)

radio3 = ctk.CTkRadioButton(diff_frame, text="Hard", variable=diff_value, value="Hard")
radio3.grid(row=1, column=2, padx=10, pady=10)

# Configure grid columns to expand equally
diff_frame.grid_columnconfigure((0, 1, 2), weight=1)

# Features Frame
features_frame = ctk.CTkFrame(frame)
features_frame.pack(padx=100, pady=5, fill="both")

check1 = ctk.CTkCheckBox(features_frame, text="Database")
check1.grid(row=0, column=0, padx=50, pady=10)

check2 = ctk.CTkCheckBox(features_frame, text="API")
check2.grid(row=0, column=1, padx=50, pady=10)

# Configure grid columns to expand equally
features_frame.grid_columnconfigure((0, 1), weight=1)

# Buttons Frame
buttons_frame = ctk.CTkFrame(frame)
buttons_frame.pack(pady=10, padx=100, fill="both")

# Generate Button
generate_button = ctk.CTkButton(buttons_frame, text="Generate Ideas", command=generate)
generate_button.grid(row=0, column=0, padx=10, pady=10)

# Save Button
save_button = ctk.CTkButton(buttons_frame, text="Save Ideas", command=save_to_file)
save_button.grid(row=0, column=1, padx=10, pady=10)

# Clear Button
clear_button = ctk.CTkButton(buttons_frame, text="Clear Ideas", command=clear_ideas)
clear_button.grid(row=0, column=2, padx=10, pady=10)

# Share via Email Button
email_button = ctk.CTkButton(buttons_frame, text="Share via Email", command=open_email_window)
email_button.grid(row=0, column=3, padx=10, pady=10)

# Configure grid columns to expand equally
buttons_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

# Result Textbox
result = ctk.CTkTextbox(root, font=ctk.CTkFont(size=15))
result.pack(pady=10, fill="x", padx=100)

# Feedback Button
feedback_button = ctk.CTkButton(root, text="Provide Feedback", command=open_feedback)
feedback_button.pack(pady=(10, 20))

root.mainloop()
