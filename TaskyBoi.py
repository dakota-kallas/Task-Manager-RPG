# Creating a window with different tabs that can be used
#
# CS 224 Team Project
# Date: 3/6/21

import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *

# global list for storing all of the tasks
task_dict = {'Hunger':0, 'Hygiene':1, 'Strength':2, 'Energy':3, 'Mood':4, 'Thirst':5}
tasks_list = [[],[],[],[],[],[]]
all_tasks = []

# global variable for couting the tasks
counter = 1
completed = 0

# global color variables
med_light = '#f4a261'
medium = '#e9c46a'
med_dark = '#2a9d8f'

def input_error() :
  # check for enter task field is empty or not
  if enter_task_field.get() == "" or clicked.get() == "Select Type":
       
      # show the error message
      messagebox.showerror("Input Error")
       
      return 0
   
  return 1

# Return the type of task. (If not found return -1)
def find_type(cur_task):
  if cur_task in tasks_list[0]:
    return 'Hunger'
  elif cur_task in tasks_list[1]:
    return 'Hygiene'
  elif cur_task in tasks_list[2]:
    return 'Strength'
  elif cur_task in tasks_list[3]:
    return 'Energy'
  elif cur_task in tasks_list[4]:
    return 'Mood'
  elif cur_task in tasks_list[5]:
    return 'Thirst'
  else:
    return -1

# Function used to mark a task complete
def complete_task():
  global counter
  global completed

  # handling the empty task error
  if counter == 1 :
    messagebox.showerror("No tasks")
    return
  
  # get the task number, which is required to delete
  number = task_number_field.get(1.0, 'end')
  
  # checking for input error when
  # empty input in task number field
  if number == "\n" :
    messagebox.showerror("Input error")
    return
  else :
    task_no = int(number)
  
  # Deleting the content of task number field
  clear_task_number_field()

  # Get the name of the current task
  cur_task = all_tasks[task_no - 1]
  task_type = ''

  # Delete from attribute list
  task_type = find_type(cur_task)
  completed += 1
  total_tasks_completed.set(completed)
  tasks_list[task_dict[task_type]].remove(cur_task)

  # deleted specified task from the list
  all_tasks.pop(task_no - 1)
 
  # decrement the counter 
  counter -= 1
     
  # whole content of text area widget is deleted
  text_area.delete(1.0, 'end')
 
  # rewriting the task after deleting one task at a time
  for i in range(len(all_tasks)) :
    text_area.insert('end -1 chars', "[ " + str(i + 1) + " ] " + all_tasks[i] + " ( " + find_type(all_tasks[i]) + " )\n")

# Function used to delete tasks
def delete_task():
  global counter

  # handling the empty task error
  if counter == 1 :
    messagebox.showerror("No tasks")
    return
  
  # get the task number, which is required to delete
  number = task_number_field.get(1.0, 'end')
  
  # checking for input error when
  # empty input in task number field
  if number == "\n" :
    messagebox.showerror("Input error")
    return
  else :
    task_no = int(number)
  
  # Deleting the content of task number field
  clear_task_number_field()

  # Get the name of the current task
  cur_task = all_tasks[task_no - 1]
  task_type = ''

  # Delete from attribute list
  task_type = find_type(cur_task)
  tasks_list[task_dict[task_type]].remove(cur_task)

  # deleted specified task from the list
  all_tasks.pop(task_no - 1)
 
  # decrement the counter 
  counter -= 1
     
  # whole content of text area widget is deleted
  text_area.delete(1.0, 'end')
 
  # rewriting the task after deleting one task at a time
  for i in range(len(all_tasks)) :
    text_area.insert('end -1 chars', "[ " + str(i + 1) + " ] " + all_tasks[i] + " ( " + find_type(all_tasks[i]) + " )\n")


# Function used to insert tasks
def insert_task():
  global counter

  # check for error
  value = input_error()
 
  # if error occur then return
  if value == 0 :
    return
  
  # get the task string concatenating
  # with new line character
  content = enter_task_field.get()
  task_type = clicked.get()
 
  # store task in the list
  tasks_list[task_dict[task_type]].append(content)
  all_tasks.append(content)
 
  # insert content of task entry field to the text area
  # add task one by one in below one by one
  text_area.insert('end -1 chars', "[ " + str(counter) + " ] " + content + " ( " + task_type + " )\n")
 
  # incremented
  counter += 1

  # Delete the contests of the input field
  clear_task_field()

# Function for clearing the contents of task entry field   
def clear_task_field():
    # clear the content of task field entry box
    enter_task_field.delete(0, 'end')

# Function for clearing the content of task number text field
def clear_task_number_field() :
  
  # clear the content of task number text field
  task_number_field.delete(0.0, 'end')

# Driver code 
if __name__ == "__main__" :

  # Create the window & instantiate its size
  win = tk.Tk()
  win.title("Tasky Boi")
  win.geometry("900x650")

  style = ttk.Style()

  light = '#ffb997'
  dark = '#f67e7d'
  
  style.theme_create( "yummy", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": light },
            "map":       {"background": [("selected", dark)],
                          "expand": [("selected", [2, 2, 2, 0])] } } } )

  style.theme_use("yummy")

  tab_parent = ttk.Notebook(win)

  # Create each tab
  tab_tasks = ttk.Frame(tab_parent)
  tab_stats = ttk.Frame(tab_parent)

  tab_parent.add(tab_tasks, text="Tasks")
  tab_parent.add(tab_stats, text="Statistics")

  # Add image file 
  bg = PhotoImage( file = r"C:\Users\Dakota\Documents\CS224\Images\background.gif") 
  
  # Show image using label 
  label1 = Label( tab_tasks, image = bg) 
  label1.place(x = 0,y = 0) 

  # create a label : Enter Your Task
  photo = PhotoImage(file = r"C:\Users\Dakota\Documents\CS224\Images\create.gif")
  enter_task = tk.Label(tab_tasks, text = "Enter Your Task", bg = med_light, font=("Trebuchet", 20))

  # create a label : My Tasks
  my_tasks = tk.Label(tab_tasks, text = "My Tasks", font=("Trebuchet", 20))
 
  # create a text entry box 
  # for typing the task
  enter_task_field = tk.Entry(tab_tasks, font=("Trebuchet", 15))

  # add image to button

  # create a Submit Button and place into the root window
  # when user press the button, the command or 
  # function affiliated to that button is executed 
  submit = tk.Button(tab_tasks, text = "Submit", fg = "Black", bg = medium, command = insert_task, font=("Trebuchet", 15))
  
  # datatype of menu text 
  clicked = StringVar() 
  
  # initial menu text 
  clicked.set( "Select Type") 

  # create options
  options = ['Hunger', 'Thirst', 'Energy', 'Strength', 'Hygiene', 'Mood']
  
  # Create Dropdown menu 
  drop = OptionMenu( tab_tasks , clicked , *options) 

  # create a text area for the root
  # with lunida 13 font
  # text area is for writing the content
  text_area = tk.Text(tab_tasks, height = 20, width = 25, font = "lucida 18")

  # create a label : Select Task Number
  task_number = tk.Label(tab_tasks, text = "Select Task Number", bg = med_light, font=("Trebuchet", 20))
                        
  task_number_field = tk.Text(tab_tasks, height = 1, width = 3, font = "lucida 18")
 
  # create a Delete & Complete Button and place into the root window
  # when user press the button, the command or 
  # function affiliated to that button is executed .
  delete = tk.Button(tab_tasks, text = "Delete", fg = "Black", bg = 'Red', command = delete_task, font=("Trebuchet", 15))
  complete = tk.Button(tab_tasks, text = "Mark Complete", fg = "Black", bg = 'Green', command = complete_task, font=("Trebuchet", 15))

  # Create a counter for the tasks completed
  tasks_completed = tk.Label(tab_tasks, text = "Tasks Completed", bg = med_light, font=("Trebuchet", 15))
  total_tasks_completed = StringVar()
  amount_tasks = tk.Label(tab_tasks, textvariable=total_tasks_completed, font=("Trebuchet", 15))

  total_tasks_completed.set(completed)

  # Create a gird of the tasks tab
  enter_task.grid(row=0, column=1, padx=15, pady=8)
  enter_task_field.grid(row=1, column=1, padx=15, pady=3)
  submit.grid(row=3, column=1, padx=15, pady=3)
  drop.grid(row=2, column=1, padx=15, pady=3)

  my_tasks.grid(row=0, column=2, padx=15, pady=8)
  text_area.grid(row=1, column=2, padx=15, pady=3, rowspan=45)

  task_number.grid(row=0, column=3, padx=15, pady=8)
  task_number_field.grid(row=1, column = 3, padx=15, pady=3)
  delete.grid(row=2, column=3, padx=15, pady=3)
  complete.grid(row=3, column=3, padx=15, pady=3)
  tasks_completed.grid(row=8, column=3, padx=15, pady=3, rowspan=20, sticky=S)
  amount_tasks.grid(row=28, column=3, padx=15, pady=3)

  tab_parent.pack(expand=1, fill="both")
  win.mainloop()