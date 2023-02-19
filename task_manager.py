# Task 21 Capstone II Compulsory Task 1

#=====importing libraries===========

from datetime import datetime
from datetime import date # Mentor Marcus advised me to keep both due to known issues when useing date only

today= date.today()
print (type(today))

#====Login Section====

# Read the username and password file
user_file = open("user.txt","r")
user_dict = {}
for line in  (user_file):
    (name, pwd) = line.split(", ")
    user_dict[name] = pwd.rstrip("\n") # remove the newline from the text file line
user_file.close()

print ("""\n
————————————————————————————————————————————
Welcome to the task manager.

Please log in to continue.
————————————————————————————————————————————""")

while True: # input and verify the username and then the password
    username =input ("\nUsername :  ")
    if not username in user_dict :
        print ("\nI'm sorry, that's not a recognised user.\n\nPlease try again.")
        continue

    pwd_entered = input (f"\nHi {username}, please enter your password : ")
    print (user_dict[username], pwd_entered, len(pwd_entered), len (user_dict[username]))
    if user_dict[username] == pwd_entered : 
        print ("\nThank you.\n")
        break
    print ("\nThat's not the correct password, please try again.") 


while True:
    # presenting the menu to the user and allow upper or lower case.
    # showing certain options only if "admin"

    print ("\nSelect one of the following options below:\n")
    if username == "admin": 
        print ('''
r - Registering a user
s - Show task statistics''')
    print ('''a - Adding a task
va - View all tasks
vm - view my task
e - Exit\n''')
    menu = input('Please enter your choice : ').lower()

    if menu == 'r' and username == "admin": # register a new user if admin logged in
        print ("""
————————————————————————————————————————————
Register a new user
""")
        # check the username doesn't already exist before creating the new user
        while True :
            new_user = input ("\nPlease enter the new username  : ")
            if new_user in user_dict :
                print ("\nThat username already exists. Please try again")
                continue
            else:
                break # if the name doesn't already exist, allow the registration to continue

        # enter and verify the password
        new_pwd = ""
        pwd_check = "-"
        while new_pwd != pwd_check :
            new_pwd = input (f"\nPlease enter the password for {new_user} : ")
            pwd_check = input (f"\nPlease re-enter the password : ")
            if new_pwd != pwd_check :
                print ("\nThe passwords do not match. Please re-enter them.")
        
        # entry is vaildated so add the user to the end of text file
        output_user = open("user.txt","a+")
        output_user.write("\n" + new_user + ", " + new_pwd)
        output_user.close()  
        print ("\nThe new user,", new_user, "has been added to the user list\n")
    
    # add a new task
    elif menu == 'a':
        # re-open and update userfile in case new users have been added to have tasks assigned to them
        user_file = open("user.txt","r")
        user_dict = {}
        for line in  (user_file):
            (name, pwd) = line.split(", ")
            user_dict[name] = pwd.rstrip("\n")
        user_file.close()
        print ("""
————————————————————————————————————————————
Add a new task
""")
        task_username = ""
        while not task_username in user_dict : # check the username exists before adding the task
            task_username = input ("\nPlease enter the username that this task is to be assigned to : ")
            if not task_username in user_dict :
                print ("\nThat user does not exist. Please try again")
        task_title = input ("\nPlease enter the title of the task : ")      
        task_desc =  input ("\nPlease enter the description of the task : ")
        
        # get and validate the task due date 
        date_format = '%d %b %Y'
        date_valid = False
        while not date_valid :
            task_due = input ("\nPlease enter the due date for this task (such as 10 Feb 2023) : ")
            try : 
                task_due = datetime.strptime(task_due, date_format).date()
                if task_due < today :
                    print ("\nTask due date must be in the future")
                    continue
                else:
                    date_valid =True 
            except ValueError:
                print ("\nIncorrect date format, please try again using the format given")

        # entry is vaildated so add the task to the tasklist
        today = today.strftime("%d %b %Y")
        task_due = task_due.strftime("%d %b %Y")
        output_user = open("tasks.txt","a+")
        output_user.write("\n" + task_username + ", " + task_title + ", " + task_desc + ", " + today + ", " + task_due + ", No")
        output_user.close()  
        print ("""
————————————————————————————————————————————
This task has been added to the tasklist
————————————————————————————————————————————""")

    # view all tasks
    elif menu == 'va': # view all tasks
        print ("""
————————————————————————————————————————————
View all tasks
""")
        task_file = open("tasks.txt","r")
        # print each task
        for task in  task_file: 
            (task_username, task_title, task_desc, task_created, task_due, task_completed) = task.split(", ")
            task_completed = task_completed.rstrip("\n") 
            print (f"""\n
————————————————————————————————————————————

Task:               {task_title}
Assigned to:        {task_username}
Date assigned:      {task_created}
Due date:           {task_due}
Task Complete?      {task_completed}
Task description:\n{task_desc}
""")
        print ("""
————————————————————————————————————————————
Task list completed/n 
————————————————————————————————————————————""")
        task_file.close()

    # view only current users tasks
    elif menu == 'vm':
        print (f"""
————————————————————————————————————————————
View all tasks for current user, {username}

""")
        task_file = open("tasks.txt","r")
        some_tasks = False # so we can check that there are some tasks for this user
        for task in  task_file: 
            (task_username, task_title, task_desc, task_created, task_due, task_completed) = task.split(", ")
            if username == task_username : 
                some_tasks= True
                task_completed = task_completed.rstrip("\n") # remove the newline from the end of text file line
                print (f"""\n
————————————————————————————————————————————

Task:               {task_title}
Date assigned:      {task_created}
Due date:           {task_due}
Task Complete?      {task_completed}
Task description:\n{task_desc}""")
        # check if any tasks have been assigned and print an appropriate response
        if some_tasks :
            print ("""
————————————————————————————————————————————
Task list completed 
————————————————————————————————————————————\n""")
        else :
            print ("""
————————————————————————————————————————————
There are no tasks for this user at present
————————————————————————————————————————————\n""")
        task_file.close()

    # show statistics if admin logged in 
    elif menu == 's' and username =='admin':
        print ('''
        ————————————————————————————————————————————
View task statistics
''')
              
        # count and show total number of tasks
        task_file = open("tasks.txt","r")
        num_tasks = 0
        for line in task_file:
            num_tasks += 1
        print('Total number of tasks : ', num_tasks)
        task_file.close()

        # count and show total number of users
        user_file = open("user.txt","r")
        num_users = 0
        for line in user_file:
            num_users += 1
        print('Total Number of users : ', num_users)
        user_file.close()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")