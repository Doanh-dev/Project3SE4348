### 12/7/2024 4:57 pm
For the program I think I will use 3 program 
1 Program is used to handle the B tree operation 
2 Program is used to handle the command
3 program is used to handle the controlflow

### 12/7/2024 5:50 pm
Creating a branch to work on the first program
Creating a model for the first program

### 12/7/2024 7:59 pm
Finish the first program
Move on to the second program

### 12/7/2024 8:12 pm
merge the main branch
push it to github
delete the branch that use for first 1 program


### 12/8/2024 12:38 am
create branch for the second program
the program shoud handle the command that assignment require like create, open,
the program command open must work perfectly so command like inset, search, load, extract can work
The program should not need to handle quit command

### 12/8/2024 2:00 am
Complete create, open, insert function
Need to do search, load, extract

### 12/8/2024 1:48 pm
Complete the second program
moving to the 3 one
need to make the menu and handle user selction choice

### 12/8/2024 2:05 pm
Create the the third branch to work on the 3 branch
merge the command -second to the 3 one
need to create a python file

### 12/8/2024 3:30 pm
Finish the main.py program
need to test and make addition if need

### 12/8/2024 7:44 pm
The main program should search the key if is already exist or not before insearching and loading
The load file should be the csv file so need to check the file before loading
Also need to promt the user about the extensiton of the index file

### 12/8/2024 8:22 pm
Fix the commandHandler program to prevent dublicate
need to test the programs

### 12/8/2024 9:17 pm
I am stating testing each command and I am looking for that the wrong printing text
It turn out, I put the wrong function for the create command

### 12/8/2024 9:22 pm
The create command was fail and I found out the error is wrong type when create a file
    in the commandHandler.py program

### 12/8/2024 9:35 pm
The insert in the btree has problem, the problame probally handle the node not problay

### 12/8/2024 9:54 pm
I figure out the erro was I close the file too early so I can not do the operation like insert, search
    print, load
My approach is changing the logic of the open the file only so I don't have to change logic 
    each other method.