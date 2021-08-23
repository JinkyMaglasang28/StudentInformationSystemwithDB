from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox

root = Tk()
root.geometry("900x550")
root.configure(bg = "#F3D1DC")
root.title("Student Information System")


def Database():

    connect = sqlite3.connect('Student.db')
    cursor = connect.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS "Course"(
            Course_Code TEXT,
            Course_Name TEXT) """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS "Students"(
            ID_number TEXT NOT NULL,
            Name TEXT   NOT NULL,
            Course  TEXT NOT NULL,
            Year_Level TEXT NOT NULL,
            Gender TEXT NOT NULL); """)

    connect.close()

    return 0

treeFrame = Frame(root)
treeFrame.grid(row=1, column=2, columnspan=3, pady=10)
treeScroll = Scrollbar(treeFrame)
treeScroll.pack(side=RIGHT, fill=Y)

tree = ttk.Treeview(treeFrame, yscrollcommand=treeScroll.set)
tree['columns'] = ('ID number', 'Name', 'Course', 'Year Level', 'Gender')

tree.column("#0", stretch=NO, width=0)
tree.column("ID number", width=120, anchor=W)
tree.column("Name", width=170, anchor=W)
tree.column("Course", width=120, anchor=W)
tree.column("Year Level", width=90, anchor=W)
tree.column("Gender", width=120, anchor=W)

tree.heading("ID number", text='ID Number', anchor=W)
tree.heading("Name", text='Name', anchor=W)
tree.heading("Course", text='Course', anchor=W)
tree.heading("Year Level", text='Year Level', anchor=W)
tree.heading("Gender", text='Gender', anchor=W)

tree.pack()
treeScroll.config(command = tree.yview)

treeFrame2 = Frame(root)
treeFrame2.grid(row=2, column=3, columnspan=3, padx=10, pady=10, sticky='w')

treeScroll2 = Scrollbar(treeFrame2)
treeScroll2.pack(side=RIGHT, fill=Y)

tree2 = ttk.Treeview(treeFrame2, yscrollcommand=treeScroll2.set)
tree2['columns'] = ('Course Code', 'Course Name')

tree2.column("#0", stretch=NO, width=0)
tree2.column("Course Code", width=120, anchor=W)
tree2.column("Course Name", width=250, anchor=W)

tree2.heading("Course Code", text='Course Code', anchor=W)
tree2.heading("Course Name", text='Course Name', anchor=W)

tree2.pack()

treeScroll2.config(command = tree2.yview)


def add_Student():

    if id_number.get() == '':
        return messagebox.showwarning("Warning!", "Please input details")
    elif name_entry.get() == '':
        return messagebox.showwarning("Warning!", "Please input details")
    elif course_entry.get() == '':
        return messagebox.showwarning("Warning!", "Please select a course")
    elif year_entry.get() == '':
        return messagebox.showwarning("Warning!", "Please select a year level")
    elif gender_entry.get() == '':
        return messagebox.showwarning("Warning!", "Please select a gender")

    conn = sqlite3.connect('Student.db')
    c = conn.cursor()

    c.execute("INSERT INTO Students VALUES (:id_number, :name, :course, :year_level, :gender)",
              {
                  'id_number': id_number.get(),
                  'name': name_entry.get(),
                  'course': course_entry.get(),
                  'year_level': year_entry.get(),
                  'gender': gender_entry.get()
              }
              )

    conn.commit()
    conn.close()
    delete_data()
    displaydata()

    return

def add():
    if ccode_entry.get() == '':
        return messagebox.showwarning("Warning!", "You haven't inputted anything")
    elif cname_entry.get() == '':
        return messagebox.showwarning("Warning!", "You haven't inputted anything")

    conn = sqlite3.connect('Student.db')
    c = conn.cursor()

    c.execute("INSERT INTO Course VALUES (:code, :name)",
              {
                  'code': ccode_entry.get(),
                  'name': cname_entry.get(),
              }
              )

    conn.commit()
    conn.close()

    add_Course()
    delete_data2()
    displaydata2()

    return

def search(e):
    for record in tree.get_children():
        tree.delete(record)

    conn = sqlite3.connect('Student.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Students WHERE ID_number=? ", (search_entry.get(),))
    records = c.fetchall()

    for i in records:
        tree.insert('', 'end', value=i)

    if search_entry.get() == '':
        delete_data()
        displaydata()
    return

def searchb():
    for record in tree.get_children():
        tree.delete(record)

    conn = sqlite3.connect('Student.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Students WHERE ID_number=? ", (search_entry.get(),))
    records = c.fetchall()

    for i in records:
        tree.insert('', 'end', value=i)

    if search_entry.get() == '':
        delete_data()
        displaydata()
    return

def delete_data():
    for record in tree.get_children():
        tree.delete(record)

def delete_data2():
    for record in tree2.get_children():
        tree2.delete(record)

def delete_Student():
    if messagebox.askyesno("Delete Confirmation", "Are you sure?") == False:
        return
    else:
        conn = sqlite3.connect("Student.db")
        c = conn.cursor()
        selected = tree.focus()
        values = tree.item(selected, 'values')


        c.execute("DELETE from Students WHERE ID_number=?", (values[0],))

        conn.commit()
        conn.close()

    delete_data()
    displaydata()

def delete():
    if messagebox.askyesno("Delete Confirmation", "Are you sure?") == False:
        return
    else:
        conn = sqlite3.connect("Student.db")
        c = conn.cursor()
        selected = tree2.focus()
        values = tree2.item(selected, 'values')

        c.execute("DELETE from Course WHERE Course_Code=?", (values[0],))

        conn.commit()
        conn.close()

    add_Course()
    delete_data2()
    displaydata2()

def update_Student():

    conn = sqlite3.connect('Student.db')
    c = conn.cursor()
    data1 = id_number.get()
    data2 = name_entry.get()
    data3 = course_entry.get()
    data4 = year_entry.get()
    data5 = gender_entry.get()

    selected = tree.selection()
    tree.item(selected, values=(data1, data2, data3, data4, data5))
    c.execute(
        "UPDATE Students set  ID_number=?, Name=?, Course=?, Year_Level=?, Gender=?  WHERE ID_number=? ",
        (data1, data2, data3, data4, data5, data1))

    conn.commit()
    conn.close()

    delete_data()
    displaydata()

def update():
    conn = sqlite3.connect('Student.db')
    c = conn.cursor()
    data1 = ccode_entry.get()
    data2 = cname_entry.get()

    selected = tree2.selection()
    tree2.item(selected, values=(data1, data2))
    c.execute(
        "UPDATE Course set  Course_Code=?, Course_Name=? WHERE Course_Code=? ",
        (data1, data2, data1))

    conn.commit()
    conn.close()

    delete_data2()
    displaydata2()

def displaydata():
    conn = sqlite3.connect('Student.db')

    c = conn.cursor()

    c.execute("SELECT * FROM Students")
    records = c.fetchall()

    global count
    count = 0

    for record in records:
        if count % 2 == 0:
            tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('evenrow',))
        else:
            tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('oddrow',))
        count += 1

    return

def displaydata2():
    conn = sqlite3.connect('Student.db')

    c = conn.cursor()

    c.execute("SELECT * FROM Course")
    records = c.fetchall()

    global count2
    count2 = 0

    for record in records:
        if count2 % 2 == 0:
            tree2.insert(parent='', index='end', iid=count2, text='', values=(record[0], record[1]), tags=('evenrow',))
        else:
            tree2.insert(parent='', index='end', iid=count2, text='', values=(record[0], record[1]), tags=('oddrow',))
        count2 += 1

    return

def clear():
    id_number.delete(0, END)
    name_entry.delete(0, END)
    course_entry.delete(0, END)
    year_entry.delete(0, END)
    gender_entry.delete(0, END)

    course_entry.set("Select Course")
    year_entry.set("Select Year Level")
    gender_entry.set("Select Gender")

def clear2():
    ccode_entry.delete(0, END)
    cname_entry.delete(0, END)

def select_record(e):
    id_number.delete(0, END)
    name_entry.delete(0, END)
    course_entry.delete(0, END)
    year_entry.delete(0, END)
    gender_entry.delete(0, END)

    selected = tree.focus()
    values = tree.item(selected, 'values')

    id_number.insert(0, values[0])
    name_entry.insert(0, values[1])
    course_entry.insert(0, values[2])
    year_entry.insert(0, values[3])
    gender_entry.insert(0, values[4])
    clear2()

def select_record2(e):
    ccode_entry.delete(0, END)
    cname_entry.delete(0, END)

    selected = tree2.focus()
    values = tree2.item(selected, 'values')

    ccode_entry.insert(0, values[0])
    cname_entry.insert(0, values[1])
    clear()

def search2(e):

    for record in tree2.get_children():
        tree2.delete(record)

    conn = sqlite3.connect('Student.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Course WHERE Course_Code=? ", (search_entry2.get(),))
    records = c.fetchall()

    for i in records:
        tree2.insert('', 'end', value=i)

    if search_entry2.get() == '':
        delete_data2()
        displaydata2()
    return

def search2b():

    for record in tree2.get_children():
        tree2.delete(record)

    conn = sqlite3.connect('Student.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Course WHERE Course_Code=? ", (search_entry2.get(),))
    records = c.fetchall()

    for i in records:
        tree2.insert('', 'end', value=i)

    if search_entry2.get() == '':
        delete_data2()
        displaydata2()
    return

def add_Course():
    ex = sqlite3.connect('Student.db')
    x = ex.cursor()

    x.execute("SELECT Course_Code FROM Course")
    rec = x.fetchall()
    xlist = []
    for i in rec:
        xlist.append(i[0])

    course_entry = ttk.Combobox(std_frame, width=18)
    course_entry.set("Select Course")
    course_entry['values'] = xlist
    course_entry.grid(row=3, column=1, pady=2)

ex = sqlite3.connect('Student.db')
x = ex.cursor()


x.execute("SELECT Course_Code FROM Course")
rec = x.fetchall()
xlist = []
for i in rec:
    xlist.append(i[0])

title_label = Label(root, text="Student  Information  System", font=("Impact", 20), fg="#F6A7C1", bg="#F3D1DC")
title_label.grid(row=0, column=0, columnspan=3, padx=10, ipadx=50)

srch = Frame(root, bg = "#FCF0CF")
srch.grid(row=0, column=4, pady=5, sticky="e")

search_entry = Entry(srch, text="Search...", borderwidth=2)
search_entry.grid(row=0, column=3, padx=10)

search_btn = Button(srch, text="Search ID Number", bg="#FCF0CF", command=searchb)
search_btn.grid(row=0, column=4, ipadx=10)


std_frame = Frame(root, bg="#FCF0CF")
std_frame.grid(row=1, column=1, padx=10)

cc_frame = Frame(root, bg="#FCF0CF")
cc_frame.grid(row=2, column=1, columnspan = 3, padx=10, sticky = 'w')

id_label = Label(std_frame, text="ID Number", bg="#FCF0CF")
id_label.grid(row=1, column=0, sticky='w', padx=5)
name_label = Label(std_frame, text="Name", bg="#FCF0CF")
name_label.grid(row=2, column=0, sticky='w', padx=5)
course_label = Label(std_frame, text="Course", bg="#FCF0CF")
course_label.grid(row=3, column=0, sticky='w', padx=5)
year_label = Label(std_frame, text="Year Level", bg="#FCF0CF")
year_label.grid(row=4, column=0, sticky='w', padx=5)
gender_label = Label(std_frame, text="Gender", bg="#FCF0CF")
gender_label.grid(row=5, column=0, sticky='w', padx=5)

cc = Label(cc_frame, text='Course Code', bg='#FCF0CF')
cc.grid(row=1, column=0, sticky='w', padx=5)
cn = Label(cc_frame, text='Course', bg='#FCF0CF')
cn.grid(row=2, column=0, sticky='w', padx=5)

id_number = Entry(std_frame, borderwidth=2)
id_number.grid(row=1, column=1, pady=2)

name_entry = Entry(std_frame, borderwidth=2)
name_entry.grid(row=2, column=1, pady=2)

course_entry = ttk.Combobox(std_frame, width=18)
course_entry.set("Select Course")
course_entry['values'] = xlist
course_entry.grid(row=3, column=1, pady=2)

"""root_gender = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    root_gender.set("Select Gender")
    root_gender['values'] = ("Male", "Female", "Other")
    root_gender.place(x=130, y=100)"""

year_entry = ttk.Combobox(std_frame, width=18)
year_entry.set("Select Year Level")
year_entry['values'] = ("1", "2", "3", "4")
year_entry.grid(row=4, column=1, pady=2)

gender_entry = ttk.Combobox(std_frame, width=18)
gender_entry.set("Select Gender")
gender_entry['values'] = ("Male", "Female", "Others")
gender_entry.grid(row=5, column=1, pady=2)

ccode_entry = Entry(cc_frame, borderwidth=2, width=26)
ccode_entry.grid(row=1, column=1, pady=2)

cname_entry = Entry(cc_frame, borderwidth=2, width=26)
cname_entry.grid(row=2, column=1, pady=2)

search_entry2 = Entry(cc_frame, borderwidth=2, width=15)
search_entry2.grid(row=0, column=2, columnspan=3, pady=40, sticky='w', padx=10)

add_btn2 = Button(cc_frame, text="Add", bg="#F3D1DC", command=add, width=7)
add_btn2.grid(row=1, column=2, sticky='e', pady=3, padx=10)

del_btn2 = Button(cc_frame, text="Delete", bg="#F3D1DC", command=delete, width=7)
del_btn2.grid(row=2, column=2, sticky='e', pady=3, padx=10)

mod_btn2 = Button(cc_frame, text="Update", bg="#F3D1DC", command=update, width=7)
mod_btn2.grid(row=1, column=3, pady=3, padx=10)

clr_btn2 = Button(cc_frame, text="Clear", bg="#F3D1DC", command=clear2, width=7)
clr_btn2.grid(row=2, column=3, pady=3, padx=10)

"""search_btn2 = Button(rightSide, text="Search Course", bg="#DAA520", command=search2, width=7)
search_btn2.grid(row=0, column=3, pady=10, ipadx=10)"""

search_btn2 = Button(cc_frame, text="Search by Course Code", bg="#F3D1DC", command=search2b)
search_btn2.grid(row=0, column=0, columnspan=2, ipadx=10, sticky='e')

add_btn = Button(std_frame, text="Add", bg="#F3D1DC", command=add_Student, width=7)
add_btn.grid(row=6, column=0, sticky='e', pady=15)

del_btn = Button(std_frame, text="Delete", bg="#F3D1DC", command=delete_Student, width=7)
del_btn.grid(row=7, column=0, sticky='e', pady=3)

upd_btn = Button(std_frame, text="Update", bg="#F3D1DC", command=update_Student, width=7)
upd_btn.grid(row=6, column=1, pady=3)

clr_btn = Button(std_frame, text="Clear", bg="#F3D1DC", command=clear, width=7)
clr_btn.grid(row=7, column=1, pady=3)


"""sel_btn = Button(leftside, text="Select", bg="#DAA520", command=select_record, width=10)
sel_btn.grid(row=7, column=1, pady=3)"""

Database()

displaydata()
displaydata2()


tree.bind("<ButtonRelease-1>", select_record)
tree2.bind("<ButtonRelease-1>", select_record2)
search_entry2.bind("<KeyRelease>", search2)
search_entry.bind("<KeyRelease>", search)

root.mainloop()
