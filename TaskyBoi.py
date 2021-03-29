# Creating a window with different tabs that can be used
#
# CS 224 Team Project
# Date: 3/6/21

import os
import math
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

# global array to hold xp values for each category
xp = [0, 0, 0, 0, 0, 0]
total_xp = 0
xp_level = 0

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
  global xp

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
  xp[task_dict[task_type]] += 10
  completed += 1
  update_xp()
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

# Function used to update the XP Statistics
def update_xp():
  global xp
  global total_xp
  global xp_level

  total_xp = 0
  for index in xp:
    total_xp += index
  
  xp_level = math.floor(total_xp/100)
  cur_xp_level.set(xp_level)
  xp_prog = math.floor(total_xp%100)
  cur_tot_xp.set(str(xp_prog) + "/100XP")

  hunger_xp.set("+ " + str(xp[task_dict['Hunger']]) + "XP")
  thirst_xp.set("+ " + str(xp[task_dict['Thirst']]) + "XP")
  strength_xp.set("+ " + str(xp[task_dict['Strength']]) + "XP")
  mood_xp.set("+ " + str(xp[task_dict['Mood']]) + "XP")
  hygiene_xp.set("+ " + str(xp[task_dict['Hygiene']]) + "XP")
  energy_xp.set("+ " + str(xp[task_dict['Energy']]) + "XP")

# Function used to change the character
def char_select():
  char_type = char_clicked.get()
  cur_dir = os.getcwd()
  img_dir = cur_dir + '/Images'
  cur_img = ''

  if char_type == 'Boy':
    cur_img = os.path.join(img_dir, 'boy.png')
  elif char_type == 'Girl':
    cur_img = os.path.join(img_dir, 'girl.png')
  elif char_type == 'Goblin':
    cur_img = os.path.join(img_dir, 'goblin.png')
  elif char_type == 'Witch':
    cur_img = os.path.join(img_dir, 'witch.png')
  elif char_type == 'Wizard':
    cur_img = os.path.join(img_dir, 'wizard.png')

  img = PhotoImage( file = cur_img) 
  character_label.configure(image=img)
  character_label.image = img

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
    enter_task_field.delete(0, 'end')

# Function for clearing the content of task number text field
def clear_task_number_field() :
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

  # Setup image files
  cur_dir = os.getcwd()
  img_dir = cur_dir + '/Images'

  # Add background image
  cur_img = os.path.join(img_dir, 'background.png')
  bg = PhotoImage( file = cur_img) 
  
  # Setup background using label 
  label1 = Label( tab_tasks, image = bg) 
  label1.place(x = 0,y = 0) 
  label2 = Label( tab_stats, image = bg)    
  label2.place(x = 0,y = 0) 
  
  # create a label : Enter Your Task
  cur_img = os.path.join(img_dir, 'create.png')
  create = PhotoImage(file = cur_img)
  enter_task = tk.Label(tab_tasks, bg = 'grey', image = create)

  # create a label : My Tasks 
  cur_img = os.path.join(img_dir, 'mytasks.png')
  my_tasks_label = PhotoImage(file = cur_img)
  my_tasks = tk.Label(tab_tasks, bg = 'grey', image = my_tasks_label)

  # create a label : My Tasks 
  cur_img = os.path.join(img_dir, 'selecttask.png')
  select_task_label = PhotoImage(file = cur_img)
  task_number = tk.Label(tab_tasks, bg = 'grey', image = select_task_label)
  
  # create a button label : Submit
  cur_img = os.path.join(img_dir, 'submit.png')
  submit_label = PhotoImage(file = cur_img)
  submit = tk.Button(tab_tasks, bg = 'grey', command = insert_task, image = submit_label)
  
  # create a button label : Delete 
  cur_img = os.path.join(img_dir, 'delete.png')
  delete_label = PhotoImage(file = cur_img)
  delete = tk.Button(tab_tasks, bg = 'grey', command = delete_task, image = delete_label)

  # create a button label : Mark Complete 
  cur_img = os.path.join(img_dir, 'markcomplete.png')
  mark_complete_label = PhotoImage(file = cur_img)
  complete = tk.Button(tab_tasks, bg = 'grey', command = complete_task, image = mark_complete_label)
 
 
  # create a text entry box 
  # for typing the task
  enter_task_field = tk.Entry(tab_tasks, font=("Trebuchet", 15))

  # add image to button

  # create a Submit Button and place into the root window
  # when user press the button, the command or 
  # function affiliated to that button is executed 
  
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
                        
  task_number_field = tk.Text(tab_tasks, height = 1, width = 3, font = "lucida 18")
  
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

  ##### Statistics Tab #####

  # create a label : Xp Level #
  xp_label = tk.Label(tab_stats, text = "XP Level", bg = med_light, font=("Trebuchet", 30))
  cur_xp_level = StringVar()
  xp_level_label = tk.Label(tab_stats, textvariable=cur_xp_level, font=("Trebuchet", 20))

  cur_xp_level.set(xp_level)

  xp_tot_label = tk.Label(tab_stats, text = "Progress", bg = med_light, font=("Trebuchet", 30))
  cur_tot_xp = StringVar()
  xp_prog_label = tk.Label(tab_stats, textvariable=cur_tot_xp, font=("Trebuchet", 20))

  cur_tot_xp.set("0/100XP")

  ## Create a dropdown for the character select ##

  # datatype of menu text 
  char_clicked = StringVar() 
  # initial menu text 
  char_clicked.set( "Select Character") 
  # create options
  char_options = ['Girl', 'Boy', 'Goblin', 'Witch', 'Wizard']
  # Create Dropdown menu 
  char_drop = OptionMenu( tab_stats , char_clicked , *char_options)
  # create a button label : Submit
  cur_img = os.path.join(img_dir, 'submit.png')
  char_submit_label = PhotoImage(file = cur_img)
  char_submit = tk.Button(tab_stats, bg = 'grey', command = char_select, image = char_submit_label)
  # character image
  cur_img = os.path.join(img_dir, 'girl.png')
  character = PhotoImage( file = cur_img) 
  character_label = tk.Label(tab_stats, bg = 'grey', image = character)


  ## Create a label for each of the task types ##
  hunger_label = tk.Label(tab_stats, text = "Hunger", bg = med_dark, font = ("Trebuchet, 30"))
  thirst_label = tk.Label(tab_stats, text = "Thirst", bg = med_dark, font = ("Trebuchet, 30"))
  energy_label = tk.Label(tab_stats, text = "Energy", bg = med_dark, font = ("Trebuchet, 30"))
  strength_label = tk.Label(tab_stats, text = "Strength", bg = med_dark, font = ("Trebuchet, 30"))
  hygiene_label = tk.Label(tab_stats, text = "Hygiene", bg = med_dark, font = ("Trebuchet, 30"))
  mood_label = tk.Label(tab_stats, text = "Mood", bg = med_dark, font = ("Trebuchet, 30"))
 
  hunger_xp = StringVar()
  hunger_xp_label = tk.Label(tab_stats, textvariable=hunger_xp, font=("Trebuchet", 15))
  hunger_xp.set("+ 0XP")

  thirst_xp = StringVar()
  thirst_xp_label = tk.Label(tab_stats, textvariable=thirst_xp, font=("Trebuchet", 15))
  thirst_xp.set("+ 0XP")

  energy_xp = StringVar()
  energy_xp_label = tk.Label(tab_stats, textvariable=energy_xp, font=("Trebuchet", 15))
  energy_xp.set("+ 0XP")
  
  strength_xp = StringVar()
  strength_xp_label = tk.Label(tab_stats, textvariable=strength_xp, font=("Trebuchet", 15))
  strength_xp.set("+ 0XP")

  hygiene_xp = StringVar()
  hygiene_xp_label = tk.Label(tab_stats, textvariable=hygiene_xp, font=("Trebuchet", 15))
  hygiene_xp.set("+ 0XP")
  
  mood_xp = StringVar()
  mood_xp_label = tk.Label(tab_stats, textvariable=mood_xp, font=("Trebuchet", 15))
  mood_xp.set("+ 0XP")
  
  # Create a grid of the statistics tab
  xp_label.grid(row=0, column = 1, padx = 75, pady = 10, columnspan = 2)
  xp_level_label.grid(row = 1, column = 1, padx = 75, pady = 10, columnspan = 2)
  xp_tot_label.grid(row=0, column = 0, padx = 75, pady = 10, columnspan = 2)
  xp_prog_label.grid(row = 1, column = 0, padx = 75, pady = 10, columnspan = 2)

  hunger_label.grid(row = 3, column = 0, padx = 75, pady = 5)
  thirst_label.grid(row = 3, column = 1, padx = 75, pady = 5)
  energy_label.grid(row = 3, column = 2, padx = 75, pady = 5)
  strength_label.grid(row = 5, column = 0, padx = 75, pady = 5)
  hygiene_label.grid(row = 5, column = 1, padx = 75, pady = 5)
  mood_label.grid(row = 5, column = 2, padx = 75, pady = 5)

  hunger_xp_label.grid(row = 4, column = 0, padx = 75, pady = 5)
  thirst_xp_label.grid(row = 4, column = 1, padx = 75, pady = 5)
  energy_xp_label.grid(row = 4, column = 2, padx = 75, pady = 5)
  strength_xp_label.grid(row = 6, column = 0, padx = 75, pady = 5)
  hygiene_xp_label.grid(row = 6, column = 1, padx = 75, pady = 5)
  mood_xp_label.grid(row = 6, column = 2, padx = 75, pady = 5)

  char_submit.grid(row = 14, column = 0, padx = 75, pady = 2, columnspan = 2)
  char_drop.grid(row = 13, column = 0, padx = 75, pady = 2, columnspan = 2)
  character_label.grid(row = 7, column = 1, padx = 75, pady = 25, rowspan = 12)

  # Complete the window
  tab_parent.pack(expand=1, fill="both")
  win.mainloop()
