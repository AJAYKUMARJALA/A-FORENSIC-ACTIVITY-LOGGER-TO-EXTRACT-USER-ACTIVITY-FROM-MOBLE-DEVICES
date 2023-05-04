from tkinter import *
from tkinter import messagebox
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import simpledialog
import tkinter
import numpy as np
from tkinter import filedialog
from bs4 import BeautifulSoup
import datetime
import pathlib
import datetime
import pytz
import docx2txt
import re
import exifread
# create the login window
root = Tk()
root.title("Login")
root.geometry("400x300")
root.resizable(False, False)
root.configure(bg="#f5f5f5")

# create a label for the title
Label(root, text="Login", font=("Arial", 24), bg="#f5f5f5").grid(row=0, column=0, columnspan=2, padx=10, pady=30)

# create a label for the username
Label(root, text="Username:", font=("Arial", 14), bg="#f5f5f5").grid(row=1, column=0, padx=10, pady=10)

# create an entry box for the username
username = Entry(root, font=("Arial", 14), bg="#fff", fg="#000")
username.grid(row=1, column=1, padx=10, pady=10)

# create a label for the password
Label(root, text="Password:", font=("Arial", 14), bg="#f5f5f5").grid(row=2, column=0, padx=10, pady=10)

# create an entry box for the password
password = Entry(root, show="*", font=("Arial", 14), bg="#fff", fg="#000")
password.grid(row=2, column=1, padx=10, pady=10)

# create a function to check login credentials and open new window
def verify_login():
    # check if username and password are correct
    if username.get() == "user" and password.get() == "pass":
        # close current window
        messagebox.showinfo("Login Successful", "Welcome, admin!")
        root.destroy()
        main = tkinter.Tk()
        main.title("A Forensics Activity Logger to Extract User Activity from Mobile Devices")
        main.geometry("1300x1200")

        global filename
        global testData
        global content

        def upload():
            global filename
            filename = filedialog.askopenfilename(initialdir="MobileData")
            pathlabel.config(text=filename)
            text.config(bg='black', fg='green', font=font1)
            text.delete('1.0', END)
            tz = pytz.timezone('Asia/Kolkata')
            current_time = datetime.datetime.now(tz)
            time_string = current_time.strftime('%Y-%m-%d %H:%M:%S')
            text.insert(END, 'ENTRY TIMING:')
            text.insert(END, time_string)
            text.insert(END, '\nFILE TYPE: HTML CHATLOG FILES, IMAGES, DOCUMENTS\n')

        # Function to extract text from the selected document and search for keywords
        def search_keywords():
            # Get the path to the selected document

            # Extract text from the document
            text = docx2txt.process(filename)

            # Get the list of keywords from the keyword entry field
            keywords = keyword_entry.get().split(",")

            # Search for the keywords in the text
            found_keywords = []
            for keyword in keywords:
                if keyword.strip() in text:
                    found_keywords.append(keyword.strip())

            # Display the list of found keywords
            if found_keywords:
                found_keywords_label.config(text=f"Found keywords: {', '.join(found_keywords)}")
            else:
                found_keywords_label.config(text="No keywords found.")

        def smail():
            my_text = docx2txt.process(filename)

            pattern = re.compile(r'[a-zA-Z0-9-\.]+@[a-zA-Z-\.]*\.(com|edu|net)')
            ph_pattern = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')


            matches = pattern.finditer(my_text)
            ph_matches = ph_pattern.finditer(my_text)
            text.delete('1.0', END)
            text.insert(END, "MAIL ID'S present in document:" + "\n\n")
            for match in matches:
                text.insert(END, "~" + match.group(0) + "\n")
            text.insert(END, "\n")
            text.insert(END, "MOBILE NUMBERS present in document:" + "\n\n")
            for match in ph_matches:
                text.insert(END, "~" + match.group(0) + "\n")
            text.insert(END, "\n")


        def eimg():
            with open(filename, 'rb') as f:
                # Get EXIF tags
                tags = exifread.process_file(f)

            # Print the tags
            text.delete('1.0', END)
            for tag in tags.keys():
                text.insert(END, f"{tag}: {tags[tag]}" + "\n")

        def extractData():
            global content
            global testData
            text.config(bg='black', fg='green', font=font1)
            text.delete('1.0', END)
            with open(filename, 'rb') as f:
                content = f.read().decode("utf-16")
            f.close()
            soup = BeautifulSoup(str(content), "html.parser")
            testData = soup.text
            text.insert(END, content)

        def forensicsActivity():
            global testData
            text.config(bg='black', fg='green', font=font1)
            text.delete('1.0', END)
            arr = testData.split("\n")
            text.insert(END, "Total lines found in file : " + str(len(arr)) + "\n")
            fname = pathlib.Path(filename)
            modify_time = datetime.datetime.fromtimestamp(fname.stat().st_mtime)
            create_time = datetime.datetime.fromtimestamp(fname.stat().st_ctime)
            size = fname.stat().st_size / 1000
            text.insert(END, "File Created Date : " + str(create_time) + "\n")
            text.insert(END, "File Last Modified Date : " + str(modify_time) + "\n")
            text.insert(END, "File size in KB : " + str(size))

        def filterData():
            global testData
            text.delete('1.0', END)
            arr = testData.split("\n")
            values = ''
            for i in range(len(arr)):
                if 'PM)' in arr[i] or 'AM)' in arr[i]:
                    values += arr[i] + "\n"
            text.insert(END, values)

        def close():
            main.destroy()

        font = ('times', 16, 'bold')
        title = Label(main, text='A Forensics Activity Logger to Extract User Activity from Mobile Devices')
        title.config(bg='black', fg='green')
        title.config(font=font)
        title.config(height=3, width=120)
        title.place(x=0, y=5)

        font1 = ('times', 13, 'bold')
        upload = Button(main, text="Upload Mobile Data", command=upload)
        upload.place(x=700, y=100)
        upload.config(font=font1)

        pathlabel = Label(main)
        pathlabel.config(bg='black', fg='green', font=font1)
        pathlabel.config(font=font1)
        pathlabel.place(x=700, y=150)

        featureextractionButton = Button(main, text="Extract Data", command=extractData)
        featureextractionButton.place(x=700, y=200)
        featureextractionButton.config(font=font1)

        featureselectionButton = Button(main, text="Apply Forensics Activity", command=forensicsActivity)
        featureselectionButton.place(x=700, y=250)
        featureselectionButton.config(font=font1)

        proposeButton = Button(main, text="Filter Data", command=filterData)
        proposeButton.place(x=700, y=300)
        proposeButton.config(font=font1)

        proposeButton = Button(main, text="Extract IMG", command=eimg)
        proposeButton.place(x=700, y=350)
        proposeButton.config(font=font1)

        proposeButton = Button(main, text="Extract MAIL/PHNO", command=smail)
        proposeButton.place(x=700, y=400)
        proposeButton.config(font=font1)

        # Create an entry field for the keywords
        keyword_entry = tkinter.Entry(main)
        keyword_entry.place(x=700, y=450)
        keyword_entry.config(font=font1)
        # Create a button to search for the keywords
        search_button = tkinter.Button(main, text="Search Keywords", command=search_keywords)
        search_button.place(x=700, y=500)
        search_button.config(font=font1)

        # Create a label to display the found keywords
        found_keywords_label = tkinter.Label(main, text="")
        found_keywords_label.place(x=700, y=550)
        found_keywords_label.config(font=font1)

        existingButton = Button(main, text="Exit", command=close)
        existingButton.place(x=700, y=650)
        existingButton.config(font=font1)

        font1 = ('times', 12, 'bold')
        text = Text(main, height=30, width=80)
        scroll = Scrollbar(text)
        text.configure(yscrollcommand=scroll.set)
        text.place(x=10, y=100)
        text.config(font=font1)

        main.config(bg='black')
        main.mainloop()

    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")


# create a login button that calls the verify_login function when clicked
Button(root, text="Login", command=verify_login, font=("Arial", 14), bg="#fff", fg="#000").grid(row=3, column=0, columnspan=2, padx=10, pady=30)

# run the window
root.mainloop()
