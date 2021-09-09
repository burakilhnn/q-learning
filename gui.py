from tkinter import *
import numpy as np

first_row = 0
first_column = 0
second_row = 0
second_column = 0

root = Tk()

e = Entry(root)
e.grid(row=0,column=0)
e1 = Entry(root)
e1.grid(row=0,column=1)
e2 = Entry(root)
e2.grid(row=1,column=0)
e3 = Entry(root)
e3.grid(row=1,column=1)


def myClick():
    first_row = int(e.get())
    first_column = int(e1.get())
    second_row = int(e2.get())
    second_column = int(e3.get())
    boxes = Label(root,text="",bg="green",width=6,height=1,borderwidth=2)
    boxes.grid(row=second_row+3,column=second_column+2,padx=2,pady=2)
    boxes = Label(root,text="",bg="yellow",width=6,height=1,borderwidth=2)
    boxes.grid(row=first_row+3,column=first_column+2,padx=2,pady=2)
    environment_rows = 25
    environment_columns = 25

    q_values = np.zeros((environment_rows, environment_columns, 4))

    actions = ['up', 'right', 'down', 'left']

    rewards = np.full((environment_rows, environment_columns), -100.)

    aisles = {}
    for j in range(1,18,9):
        aisles[j] = [i for i in range(1, 20)]
        aisles[j+1] = [1, 7, 9,11,17,19,21]
        aisles[j+2] = [i for i in range(1, 25)]
        aisles[j+2].remove(8)
        aisles[j+3] = [3, 7,13,17,23]
        aisles[j+4] = [i for i in range(25)]
        aisles[j+5] = [5,15]
        aisles[j+6] = [i for i in range(1, 20)]
        aisles[j+7] = [3, 7,13,17,23]
        aisles[j+8] = [i for i in range(25)]
    aisles[19] = [i for i in range(1, 20)]
    aisles[20] = [1, 7, 9,11,17,19,21]
    aisles[21] = [i for i in range(1, 25)]
    aisles[21].remove(8)
    aisles[22] = [3,7,13,17,23]
    aisles[23] = [i for i in range(25)]
    aisles[24] = [5,15]
    for row_index in range(1, 25):
      for column_index in aisles[row_index]:
        rewards[row_index, column_index] = -1.
  
    rewards[second_row, second_column] = 100. 
    def is_terminal_state(current_row_index, current_column_index):
      if rewards[current_row_index, current_column_index] == -1.:
        return False
      else:
        return True

    def get_starting_location():
      current_row_index = np.random.randint(environment_rows)
      current_column_index = np.random.randint(environment_columns)
      while is_terminal_state(current_row_index, current_column_index):
        current_row_index = np.random.randint(environment_rows)
        current_column_index = np.random.randint(environment_columns)
      return current_row_index, current_column_index

    def get_next_action(current_row_index, current_column_index, epsilon):
      if np.random.random() < epsilon:
        return np.argmax(q_values[current_row_index, current_column_index])
      else: 
        return np.random.randint(4)

    def get_next_location(current_row_index, current_column_index, action_index):
      new_row_index = current_row_index
      new_column_index = current_column_index
      if actions[action_index] == 'up' and current_row_index > 0:
        new_row_index -= 1
      elif actions[action_index] == 'right' and current_column_index < environment_columns - 1:
        new_column_index += 1
      elif actions[action_index] == 'down' and current_row_index < environment_rows - 1:
        new_row_index += 1
      elif actions[action_index] == 'left' and current_column_index > 0:
        new_column_index -= 1
      return new_row_index, new_column_index

    def get_shortest_path(start_row_index, start_column_index):
      if is_terminal_state(start_row_index, start_column_index):
        return []
      else: 
        current_row_index, current_column_index = start_row_index, start_column_index
        shortest_path = []
        shortest_path.append([current_row_index, current_column_index])
    
        while not is_terminal_state(current_row_index, current_column_index):
          action_index = get_next_action(current_row_index, current_column_index, 1.)
          current_row_index, current_column_index = get_next_location(current_row_index, current_column_index, action_index)
          shortest_path.append([current_row_index, current_column_index])
        return shortest_path

    epsilon = 0.9
    discount_factor = 0.9
    learning_rate = 0.9

    for episode in range(1000):
      row_index, column_index = get_starting_location()
      while not is_terminal_state(row_index, column_index):
        action_index = get_next_action(row_index, column_index, epsilon)
        old_row_index, old_column_index = row_index, column_index 
        row_index, column_index = get_next_location(row_index, column_index, action_index)
        reward = rewards[row_index, column_index]
        old_q_value = q_values[old_row_index, old_column_index, action_index]
        temporal_difference = reward + (discount_factor * np.max(q_values[row_index, column_index])) - old_q_value
        new_q_value = old_q_value + (learning_rate * temporal_difference)
        q_values[old_row_index, old_column_index, action_index] = new_q_value

    path = get_shortest_path(first_row, first_column)
    print(path)
    length = len(path) - 1
    for i in range(1,length):
      a = path[i][0]
      b = path[i][1]
      boxes = Label(root,text="",bg="black",width=6,height=1,borderwidth=2)
      boxes.grid(row=a+3,column=b+2,padx=2,pady=2)

myButton = Button(root,text="Enter Points",command=myClick)
myButton.grid(row=2)
file = open("engel.txt", "w")
for i in range(3,28):
    for j in range(2,27):
        boxes = Label(root,text="",bg="red",width=6,height=1,borderwidth=2)
        boxes.grid(row=i,column=j,padx=2,pady=2)

for i in range(4,23,9):
    for j in range(3,22):
        boxes = Label(root,text="",bg="white",width=6,height=1,borderwidth=2)
        boxes.grid(row=i,column=j,padx=2,pady=2)
        color = "B"
        row = str(i-3)
        col = str(j-2)
        file.write("" + row + "," + col + "," +color+"\n")
        

for i in range(5,24,9):
    for j in range(3,27):
        row = str(i-3)
        col = str(j-2)
        if j == 3 or j ==9 or j ==11 or j ==13 or j ==19 or j ==21 or j ==23:
            boxes = Label(root,text="",bg="white",width=6,height=1,borderwidth=2)
            boxes.grid(row=i,column=j,padx=2,pady=2)
            color = "B"
        else:
          color = "K"
        file.write("" + row + "," + col + "," +color+"\n")

for i in range(6,25,9):
    for j in range(3,27):
        row = str(i-3)
        col = str(j-2)
        if j != 10:
            boxes = Label(root,text="",bg="white",width=6,height=1,borderwidth=2)
            boxes.grid(row=i,column=j,padx=2,pady=2)
            color = "B"
        else:
          color = "K"
        file.write("" + row + "," + col + "," +color+"\n")

for i in range(7,26,9):
    for j in range(2,27):
        row = str(i-3)
        col = str(j-2)
        if j == 5 or j == 9 or j==15 or j==19 or j==25:
            boxes = Label(root,text="",bg="white",width=6,height=1,borderwidth=2)
            boxes.grid(row=i,column=j,padx=2,pady=2)
            color = "B"
        else:
          color = "K"
        file.write("" + row + "," + col + "," +color+"\n")
      

for i in range(8,27,9):
    for j in range(2,27):
        boxes = Label(root,text="",bg="white",width=6,height=1,borderwidth=2)
        boxes.grid(row=i,column=j,padx=2,pady=2)
        row = str(i-3)
        col = str(j-2)
        color = "B"
        file.write("" + row + "," + col + "," +color+"\n")


for i in range(9,28,9):
    for j in range(2,27):
        row = str(i-3)
        col = str(j-2)
        if j == 7 or j == 17:
            boxes = Label(root,text="",bg="white",width=6,height=1,borderwidth=2)
            boxes.grid(row=i,column=j,padx=2,pady=2)
            color = "B"
        else:
          color = "K"
        file.write("" + row + "," + col + "," +color+"\n")
      

for i in range(10,20,9):
    for j in range(3,22):
        boxes = Label(root,text="",bg="white",width=6,height=1,borderwidth=2)
        boxes.grid(row=i,column=j,padx=2,pady=2)
        row = str(i-3)
        col = str(j-2)
        color = "B"
        file.write("" + row + "," + col + "," +color+"\n")
            
for i in range(11,21,9):
    for j in range(2,27):
        row = str(i-3)
        col = str(j-2)
        if j == 5 or j == 9 or j==15 or j==19 or j==25:
            boxes = Label(root,text="",bg="white",width=6,height=1,borderwidth=2)
            boxes.grid(row=i,column=j,padx=2,pady=2)
            color = "B"
        else:
          color = "K"
        file.write("" + row + "," + col + "," +color+"\n")

for i in range(12,22,9):
    for j in range(2,27):
        boxes = Label(root,text="",bg="white",width=6,height=1,borderwidth=2)
        boxes.grid(row=i,column=j,padx=2,pady=2)
        row = str(i-3)
        col = str(j-2)
        color = "B"
        file.write("" + row + "," + col + "," +color+"\n")


root.mainloop()
