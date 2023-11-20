import datetime
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3

connector = sqlite3.connect('TeacherManagement.db')
cursor = connector.cursor()
connector.execute(
    "CREATE TABLE IF NOT EXISTS TEACHER_MANAGEMENT (TEACHER_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, AGE INTEGER, DOB TEXT, CLASSES INTEGER)"
)


def add_teacher_record():
    global name_strvar, age_strvar, dob, classes_strvar
    name = name_strvar.get()
    age = age_strvar.get()
    dob_value = dob.get_date()
    classes = classes_strvar.get()

    if not name or not age or not dob_value or not classes:
        mb.showerror("Error!", "Please fill all the fields")
    else:
        try:
            connector.execute(
                'INSERT INTO TEACHER_MANAGEMENT (NAME, AGE, DOB, CLASSES) VALUES (?,?,?,?)',
                (name, age, dob_value, classes)
            )
            connector.commit()
            mb.showinfo('Record added', f"Record of {name} was successfully added")
            clear_fields()
            display_teacher_records()
        except:
            mb.showerror('Wrong type', 'Ensure the values entered are correct.')


def clear_fields():
    global name_strvar, age_strvar, dob, classes_strvar
    for var in [name_strvar, age_strvar, classes_strvar]:
        var.set('')
    dob.set_date(datetime.datetime.now().date())


def clear_form():
    global tree
    tree.delete(*tree.get_children())
    clear_fields()


def display_teacher_records():
    tree.delete(*tree.get_children())
    curr = connector.execute('SELECT * FROM TEACHER_MANAGEMENT')
    data = curr.fetchall()
    for records in data:
        tree.insert('', END, values=records)


def remove_teacher_record():
    if not tree.selection():
        mb.showerror('Select a teacher')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]
        tree.delete(current_item)
        connector.execute('DELETE FROM TEACHER_MANAGEMENT WHERE TEACHER_ID=%d' % selection[0])
        connector.commit()
        mb.showinfo('Done', 'The teacher record was successfully deleted.')
        display_teacher_records()


def view_teacher_record():
    global name_strvar, age_strvar, dob, classes_strvar
    if not tree.selection():
        mb.showerror('Select a teacher record to view')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]

        name_strvar.set(selection[1])
        age_strvar.set(selection[2])
        dob_value = datetime.date(int(selection[3][:4]), int(selection[3][5:7]), int(selection[3][8:]))
        dob.set_date(dob_value)
        classes_strvar.set(selection[4])


def filter_teachers():
    age_filter = age_filter_var.get()
    classes_filter = classes_filter_var.get()

    if not age_filter and not classes_filter:
        display_teacher_records()
        return

    tree.delete(*tree.get_children())

    query = 'SELECT * FROM TEACHER_MANAGEMENT WHERE '
    conditions = []

    if age_filter:
        conditions.append(f'AGE = {age_filter}')

    if classes_filter:
        conditions.append(f'CLASSES = {classes_filter}')

    query += ' AND '.join(conditions)

    curr = connector.execute(query)
    data = curr.fetchall()
    for records in data:
        tree.insert('', END, values=records)


def calculate_average_classes():
    curr = connector.execute('SELECT AVG(CLASSES) FROM TEACHER_MANAGEMENT')
    average_classes = curr.fetchone()[0]
    mb.showinfo('Average Classes', f'The average number of classes is: {average_classes:.2f}')


headlabelfont = ("Arial", 20, 'bold')
labelfont = ('Verdana', 12)
entryfont = ('Verdana', 12, 'italic')

main = Tk()
main.geometry('1000x600')
main.resizable(0, 0)

lf_bg = '#8BC34A'  
cf_bg = '#CDDC39'
button_bg = '#2196F3'  
button_fg = 'white'
entry_bg = 'white'
entry_fg = 'black'

name_strvar = StringVar()
age_strvar = StringVar()
classes_strvar = StringVar()

left_frame = Frame(main, bg=lf_bg)
left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)

center_frame = Frame(main, bg=cf_bg)
center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)

right_frame = Frame(main, bg="#607D8B")
right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)

Label(left_frame, text="Name", font=labelfont, bg=lf_bg, fg='white').place(relx=0.375, rely=0.05)
Label(left_frame, text="Age", font=labelfont, bg=lf_bg, fg='white').place(relx=0.3, rely=0.18)
Label(left_frame, text="Date of Birth (DOB)", font=labelfont, bg=lf_bg, fg='white').place(relx=0.1, rely=0.31)
Label(left_frame, text="Number of Classes", font=labelfont, bg=lf_bg, fg='white').place(relx=0.1, rely=0.44)

Entry(left_frame, width=19, textvariable=name_strvar, font=entryfont, bg=entry_bg, fg=entry_fg).place(x=20, rely=0.1)
Entry(left_frame, width=19, textvariable=age_strvar, font=entryfont, bg=entry_bg, fg=entry_fg).place(x=20, rely=0.23)
Entry(left_frame, width=19, textvariable=classes_strvar, font=entryfont, bg=entry_bg, fg=entry_fg).place(x=20, rely=0.57)

dob = DateEntry(left_frame, font=("Arial", 12), width=15, bg='#4CAF50', fg='white', borderwidth=2, relief="groove")
dob.place(x=20, rely=0.36)

Button(left_frame, text='Add Record', font=labelfont, command=add_teacher_record, width=18, bg=button_bg,
       fg=button_fg).place(relx=0.025, rely=0.75)

Button(center_frame, text='Delete Record', font=labelfont, command=remove_teacher_record, width=15, bg=button_bg,
       fg=button_fg).place(relx=0.1, rely=0.25)
Button(center_frame, text='View Record', font=labelfont, command=view_teacher_record, width=15, bg=button_bg,
       fg=button_fg).place(relx=0.1, rely=0.35)
Button(center_frame, text='Reset Fields', font=labelfont, command=clear_fields, width=15, bg=button_bg,
       fg=button_fg).place(relx=0.1, rely=0.45)
Button(center_frame, text='Delete Database', font=labelfont, command=clear_form, width=15, bg=button_bg,
       fg=button_fg).place(relx=0.1, rely=0.55)

Label(center_frame, text='Filter by Age:', font=labelfont, bg=cf_bg, fg='white').place(relx=0.1, rely=0.65)
Label(center_frame, text='Filter by Classes:', font=labelfont, bg=cf_bg, fg='white').place(relx=0.1, rely=0.75)

age_filter_var = StringVar()
classes_filter_var = StringVar()

Entry(center_frame, width=10, textvariable=age_filter_var, font=entryfont, bg=entry_bg, fg=entry_fg).place(relx=0.3,
                                                                                                           rely=0.70)
Entry(center_frame, width=10, textvariable=classes_filter_var, font=entryfont, bg=entry_bg, fg=entry_fg).place(
    relx=0.3, rely=0.79)

Button(center_frame, text='Filter', font=labelfont, command=filter_teachers, width=15, bg=button_bg,
       fg=button_fg).place(relx=0.1, rely=0.84)
Button(center_frame, text='Average Classes', font=labelfont, command=calculate_average_classes, width=15, bg=button_bg,
       fg=button_fg).place(relx=0.1, rely=0.15)


Label(right_frame, text='Teachers Records', font=headlabelfont, bg='#607D8B', fg='white').pack(side=TOP, fill=X)
tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                    columns=('Teacher ID', "Name", "Age", "Date of Birth", "Number of Classes"), show="headings")
X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)
tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)
tree.heading('Teacher ID', text='ID', anchor=CENTER)
tree.heading('Name', text='Name', anchor=CENTER)
tree.heading('Age', text='Age', anchor=CENTER)
tree.heading('Date of Birth', text='DOB', anchor=CENTER)
tree.heading('Number of Classes', text='Classes', anchor=CENTER)
tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=40, stretch=NO)
tree.column('#2', width=140, stretch=NO)
tree.column('#3', width=80, stretch=NO)
tree.column('#4', width=120, stretch=NO)
tree.column('#5', width=150, stretch=NO)
tree.place(y=30, relwidth=1, relheight=0.9, relx=0)
display_teacher_records()

main.mainloop()
