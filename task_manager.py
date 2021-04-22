# A task manager combined with an Role-Playing Game.
#
# Authors: Dakota Kallas, Chase Roehl, Cailyn Paul
# Date: 4/22/21

import os
from os import path
import math
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
import requests
import json

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

def name_error() :
  # check for enter task field is empty or not
  if name_field.get() == "":
       
      # show the error message
      messagebox.showerror("Invalid Name Error")
       
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

# Check to ensure a valid user input
def check_user_input(input):
  global counter

  # handling the empty task error
  if counter == 1 :
    messagebox.showerror("Error", "No tasks")
    return

  # checking for input error when
  # empty input in task number field
  if input == "\n" :
    messagebox.showerror("Error", "Input error")
    return False

  try:
    # Convert it into integer
    input = int(input)
  except ValueError:
    messagebox.showerror("Error", "Input error")
    return False

  # checking for input error when
  # input is greater than total tasks
  if input >= counter :
    messagebox.showerror("Error", "Input too high")
    return False

  return True

# Function used to mark a task complete
def complete_task():
  global counter
  global completed
  global xp

  # get the task number, which is required to delete
  number = task_number_field.get(1.0, 'end')
  
  if check_user_input(number) == False:
    return
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

  # get the task number, which is required to delete
  number = task_number_field.get(1.0, 'end')
  
  if check_user_input(number) == False:
    return
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

# Function for generating a random task
def insert_random_task():
  global counter
  # Gets the task from the api 
  response = requests.get('https://www.boredapi.com/api/activity/')
  decode_response = json.loads(response.content.decode('utf-8'))
  task = decode_response.get('activity')

  # Add task to the mood task list
  tasks_list[4].append(task)
  all_tasks.append(task)

  # Insert it into the text area 
  text_area.insert('end -1 chars', "[ " + str(counter) + " ] " + task + " ( Mood )\n")

  # add 1 to the counter
  counter += 1

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

# Check to see if the program has previous data
def data_check():
  if path.exists("data.txt"):
    return True
  else:
    return False

# Create a data file and begin to store important information in it
def create_data():
  lines = []
  lines.append("Girl\n")  # Default character
  lines.append("0\n") # Tasks Completed
  lines.append("0\n") # Overall XP
  lines.append("0\n") # Hunger XP
  lines.append("0\n") # Hygiene XP
  lines.append("0\n") # Strength XP
  lines.append("0\n") # Energy XP
  lines.append("0\n") # Mood XP
  lines.append("0\n") # Thirst XP
  f = open("data.txt", "w")
  f.writelines(lines)
  f.close()

def read_data():
  global xp, completed, task_dict, counter, all_tasks, tasks_list

  # Read in the data
  f = open("data.txt", "r")
  lines =  f.readlines()
  f.close()

  # Update the character
  char_type = lines[0].strip()
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

  # Update the XP
  xp[task_dict['Hunger']] = int(lines[3].strip())
  xp[task_dict['Hygiene']] = int(lines[4].strip())
  xp[task_dict['Strength']] = int(lines[5].strip())
  xp[task_dict['Energy']] = int(lines[6].strip())
  xp[task_dict['Mood']] = int(lines[7].strip())
  xp[task_dict['Thirst']] = int(lines[8].strip())
  update_xp()

  # Update the tasks
  completed = int(lines[1].strip())
  total_tasks_completed.set(completed)

  if len(lines) > 9:
    cur = 9
    while cur < len(lines):
      cur_task = lines[cur].strip().split()

      # get the task string concatenating
      # with new line character
      task_type = cur_task[0]
      content = ''
      word = 1
      for e in cur_task[1:]:
        if word == 1:
          content += e
        else:
          content += " " + e
        word += 1
 
      # store task in the list
      tasks_list[task_dict[task_type]].append(content)
      all_tasks.append(content)
 
      # insert content of task entry field to the text area
      # add task one by one in below one by one
      text_area.insert('end -1 chars', "[ " + str(counter) + " ] " + content + " ( " + task_type + " )\n")
 
      # incremented
      counter += 1
      cur += 1

# Safely save the program by saving all of the data within
def save():
  global xp, total_xp, completed, tasks_list
  char_type = char_clicked.get()

  # Update the data file
  f = open("data.txt", "r")
  lines =  f.readlines()
  f.close()

  if char_type == "Select Character":
    char_type = lines[0].strip()

  lines[0] = char_type + "\n"
  lines[1] = str(completed) + "\n"
  lines[2] = str(total_xp) + "\n"
  lines[3] = str(xp[task_dict['Hunger']]) + "\n"
  lines[4] = str(xp[task_dict['Hygiene']]) + "\n"
  lines[5] = str(xp[task_dict['Strength']]) + "\n"
  lines[6] = str(xp[task_dict['Energy']]) + "\n"
  lines[7] = str(xp[task_dict['Mood']]) + "\n"
  lines[8] = str(xp[task_dict['Thirst']]) + "\n"

  if len(lines) > 9:
    del lines[9:]

  for i in range(len(tasks_list)):
    for task in tasks_list[i]:
      task_type = ''
      if i == 0:
        task_type = 'Hunger'
      elif i == 1:
        task_type = 'Hygiene'
      elif i == 2:
        task_type = 'Strength'
      elif i == 3:
        task_type = 'Energy'
      elif i == 4:
        task_type = 'Mood'
      elif i == 5:
        task_type = 'Thirst'
      lines.append(task_type + " " + task + "\n")

  f = open("data.txt", "w")
  lines =  f.writelines(lines)
  f.close()

# Driver code 
if __name__ == "__main__" :
  
  # Create the window & instantiate its size
  win = tk.Tk()
  win.title("Task Manager by DK, CR, and CP")
  win.geometry("900x680")

  style = ttk.Style()

  light = '#ffb997'
  dark = '#4d3620'
  
  style.theme_create( "tasky", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": light },
            "map":       {"background": [("selected", dark)],
                          "expand": [("selected", [2, 2, 2, 0])] } } } )

  style.theme_use("tasky")

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

  # create a button : Tasks Completed
  cur_img = os.path.join(img_dir, 'taskscompleted.png')
  task_completed_label = PhotoImage(file = cur_img)
  tasks_completed = tk.Label(tab_tasks, bg = 'grey', image = task_completed_label)
  
  # create a button label : Submit
  # when user press the button, the command or 
  # function affiliated to that button is executed 
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
 
  # create a button label : Save
  cur_img = os.path.join(img_dir, 'save.png')
  save_label = PhotoImage(file = cur_img)
  save_button = tk.Button(tab_tasks, bg = 'grey', command = save, image = save_label)
 
  # create a text entry box for typing the task
  enter_task_field = tk.Entry(tab_tasks, font=("Trebuchet", 15))
  
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
  total_tasks_completed = StringVar()
  amount_tasks = tk.Label(tab_tasks, textvariable=total_tasks_completed, font=("Trebuchet", 15))

  total_tasks_completed.set(completed)

  # Create a button: Bored?
  cur_img = os.path.join(img_dir, 'bored.png')
  bored_label = PhotoImage(file = cur_img)
  bored_button = tk.Button(tab_tasks, bg = 'grey', command = insert_random_task, image = bored_label)

  # Create a gird of the tasks tab
  enter_task.grid(row=0, column=1, padx=15, pady=8)
  enter_task_field.grid(row=1, column=1, padx=15, pady=3)
  submit.grid(row=3, column=1, padx=15, pady=3)
  drop.grid(row=2, column=1, padx=15, pady=3)
  bored_button.grid(row=28, column=1, padx=15, pady=8)

  my_tasks.grid(row=0, column=2, padx=15, pady=8)
  text_area.grid(row=1, column=2, padx=15, pady=3, rowspan=45)

  task_number.grid(row=0, column=3, padx=15, pady=8)
  task_number_field.grid(row=1, column = 3, padx=15, pady=3)
  delete.grid(row=2, column=3, padx=15, pady=3)
  complete.grid(row=3, column=3, padx=15, pady=3)
  tasks_completed.grid(row=8, column=3, padx=15, pady=3, rowspan=20, sticky=S)
  amount_tasks.grid(row=28, column=3, padx=15, pady=3)
  save_button.grid(row=40, column=3, padx=15, pady=3)

  ##### Statistics Tab #####

  # create a label : Xp Level
  cur_img = os.path.join(img_dir, 'xplevel.png')
  xp_level_img = PhotoImage(file = cur_img)
  xp_label = tk.Label(tab_stats, bg = dark, image = xp_level_img)
  cur_xp_level = StringVar()
  xp_level_label = tk.Label(tab_stats, textvariable=cur_xp_level, font=("Trebuchet", 20))

  cur_xp_level.set(xp_level)

  cur_img = os.path.join(img_dir, 'progress.png')
  progress_img = PhotoImage(file = cur_img)
  xp_tot_label = tk.Label(tab_stats, bg = dark, image = progress_img)
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
  cur_img = os.path.join(img_dir, 'hunger.png')
  hunger_img = PhotoImage(file = cur_img)
  hunger_label = tk.Label(tab_stats, bg = dark, image = hunger_img)

  cur_img = os.path.join(img_dir, 'thirst.png')
  thirst_img = PhotoImage(file = cur_img)
  thirst_label = tk.Label(tab_stats, bg = dark, image = thirst_img)

  cur_img = os.path.join(img_dir, 'energy.png')
  energy_img = PhotoImage(file = cur_img)
  energy_label = tk.Label(tab_stats, bg = dark, image = energy_img)

  cur_img = os.path.join(img_dir, 'strength.png')
  strength_img = PhotoImage(file = cur_img)
  strength_label = tk.Label(tab_stats, bg = dark, image = strength_img)

  cur_img = os.path.join(img_dir, 'hygiene.png')
  hygiene_img = PhotoImage(file = cur_img)
  hygiene_label = tk.Label(tab_stats, bg = dark, image = hygiene_img)

  cur_img = os.path.join(img_dir, 'mood.png')
  mood_img = PhotoImage(file = cur_img)
  mood_label = tk.Label(tab_stats, bg = dark, image = mood_img)
 
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

  # Check to see if the program has previous data
  data = data_check()
  if data == False:
    create_data()
  else:
    read_data()

  # Complete the window
  tab_parent.pack(expand=1, fill="both")
  win.mainloop()
