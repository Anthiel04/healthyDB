import os
import sys
from menu import Menu as m


def main():
    file_path = input("Provide the file path: ")

    if os.path.isfile(file_path):
        menu = m(file_path)
        menu.main()
    else:
        print("File not found")

if __name__ == "__main__":
    main()
