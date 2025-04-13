import os

def save_file(content, file_path):
    with open(file_path, "w") as file:
        file.write(content)

def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()