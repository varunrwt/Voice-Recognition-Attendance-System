import speech_recognition as sr
import csv
from datetime import date
import tkinter as tk
import re
from tkinter import *
import os
import pandas as pd


# Initialize the recognizer
r = sr.Recognizer()

def record_audio():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

def mark_attendance(student_id):
    today = date.today()
    with open('attendance.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([today, student_id])
        output_text.insert(tk.END, f"Attendance marked for student ID: {student_id}\n")

def recognize_speech():
    while True:
        text = record_audio()
        if text is not None:
            if re.match("stop",text):
                print('listening stopped')
                break
            else:
                mark_attendance(text)
                

def start_attendance():
    recognize_speech()
def d_row():
    df = pd.read_csv('attendance.csv')
    df.drop(df[df['Name'] == s_name.get()].index, inplace = True)
    df.to_csv('attendance.csv',columns=["Date","Name"],index=False)
    print("attendance deleted")

def delete():
    global delete_records
    delete_records = Toplevel(succesful_login)
    delete_records.geometry("500x300")
    Label(delete_records,text="enter the name",bg="white",fg="green").pack(fill=X,pady=20)
    global s_name 
    s_name = StringVar()
    student_name = Entry(delete_records,textvariable=s_name)
    student_name.pack(pady=20)
    Button(delete_records,text="delete_attendance",command = d_row).pack(pady=20)   
    Button(delete_records,text="close",command=lambda: delete_records.destroy()).pack(pady=20)

def adding():
    with open('attendance.csv',mode='a',newline='') as f_object:
        writer_object = csv.writer(f_object)
        writer_object.writerow([d_date.get(),d_name.get()])
    f_object.close()
    print("manual entry succesful")

def add():
    global add_records
    add_records = Toplevel(succesful_login)
    add_records.geometry("500x400")
    global d_name
    d_name = StringVar()
    global d_date
    d_date = StringVar()
    Label(add_records,text="enter the name",bg="white",fg="green").pack(pady=20)
    e1=Entry(add_records,textvariable=d_name)
    e1.pack(pady=20)
    Label(add_records,text="enter the date",bg="white",fg="green").pack(pady=20)
    e2=Entry(add_records,textvariable=d_date)
    e2.pack(pady=20)
    Button(add_records,text="add",command=adding).pack(pady=20)
    Button(add_records,text="close",command=lambda:add_records.destroy()).pack(pady=20)
 
def records():
    global records_window
    records_window = Toplevel(succesful_login)
    records_window.title("attendance_records")
    records_window.geometry("300x300")
    o_text = tk.Text(records_window, height=50, width=30)
    o_text.pack(pady=20)
    with open("attendance.csv", "r") as csv_file:
      reader = csv.DictReader(csv_file)
      for row in reader:
         o_text.insert(tk.END,row['Date']+"   "+row['Name']+"\n")
   
   

def next():
        person_exist = False
        for line in open("credentials.txt","r").readlines():
             login_values = line.split()
             if(login_values[1] == l_username.get() and login_values[3] == l_password.get()):
                  person_exist = True
        if person_exist:
             login_username_entry.delete(0,END)
             login_password_entry.delete(0,END)
             global succesful_login
             succesful_login = Toplevel(login_window)
             succesful_login.geometry("200x300")
             succesful_login.title("succesful login")
             Button(succesful_login,text="add_manual_attendance",command=add).pack(pady=20)
             Button(succesful_login,text="delete_attendance",command=delete).pack(pady=20)
             Button(succesful_login,text="attendance_records",command=records).pack(pady=20)
             Button(succesful_login,text="close",command=lambda :succesful_login.destroy()).pack(pady=20)
        else:
             login_username_entry.delete(0,END)
             login_password_entry.delete(0,END)
             failed_login = Toplevel(login_window)
             failed_login.geometry("200x200")
             failed_login.title("failed login")
             Label(failed_login,text="failed to login!!!",bg="white",fg="red").pack(fill=X,pady=20)
             Button(failed_login,text="OK",command = lambda:failed_login.destroy()).pack(pady=20)   

def login():
        global login_window
        global l_username
        l_username = StringVar()
        global l_password
        l_password = StringVar()
        login_window = Toplevel(window)
        login_window.geometry("300x300")
        login_panel = Frame(login_window)
        login_panel.pack(pady=20)
        Label(login_panel,text="Username: ",bg="white",fg="black").grid(row=0,column=0)
        global login_username_entry
        login_username_entry=Entry(login_panel,textvariable=l_username)
        login_username_entry.grid(row=0,column=1)
        Label(login_panel,text="").grid(row=1)
        Label(login_panel,text="Password: ",bg="white",fg="black").grid(row=2,column=0)
        global login_password_entry
        login_password_entry=Entry(login_panel,textvariable=l_password)
        login_password_entry.grid(row=2,column=1)
        Label(login_panel,text="").grid(row=3)
        Button(login_window,text="Login",command=next).pack(pady=20)
        Button(login_window,text="close",command=lambda: login_window.destroy()).pack(pady=20)



# Create the main window
window = tk.Tk()
window.title("Attendance Management System")

# Create the GUI elements
start_button = tk.Button(window, text="Start Attendance", command=start_attendance)
loginv = tk.Button(window, text="Admin", command=login)
loginv.pack(pady=10)
start_button.pack(pady=10)
output_text = tk.Text(window, height=10, width=30)
output_text.pack(pady=10)
Button(window,text="close",command=lambda: exit()).pack(pady=20)

# Run the main window loop
window.mainloop()