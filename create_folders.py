import os

current_directory = os.getcwd()

#for char in "abcdefghijklmnopqrstuvwxyz":
#    char = f'^{char}'
#    os.makedirs(os.path.join(current_directory, char), exist_ok=True)

for i in range(0, 10):
    i = str(i)
    os.makedirs(os.path.join(current_directory, i), exist_ok=True)

created_directories_current = os.listdir(current_directory)
created_directories_current.sort()
created_directories_current