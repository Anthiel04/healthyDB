import time
import sys

from dbhelpers import DbHelpers as dbh
from soft_clean import SC as sc
from hard_clean import HC as hc

class Menu:
    def __init__(self,file_path):
        self.option = ""
        self.file_path = file_path
        
        
    def option_2(self):
        print(f"Hard Cleaning in progress...")
        start = time.time()
        try:
            print(f"Processing file: {self.file_path}")

            cure = hc(dbh(self.file_path))
            cure.main()

            end = time.time()
            cure.tools.report.update_report("time", end-start)
            print(f"Done in {end - start} seconds")
        except FileNotFoundError:
            print(f"File {self.file_path} not found.")
            self.main()

        except Exception as e:
            print(f"Something went wrong: {e}")
            sys.exit(1)


    def option_1(self):
        print("Soft Cleaning in progress...")
        start = time.time()
        try:
            print(f"Processing file: {self.file_path}")

            cure = sc(dbh(self.file_path))
            cure.main()

            end = time.time()
            cure.tools.report.update_report("time", end-start)
            print(f"Done in {end - start} seconds")
        except FileNotFoundError:
            print(f"File {self.file_path} not found.")
            self.main()

        except Exception as e:
            print(f"Something went wrong: {e}")
            sys.exit(1)

    def main(self):
        print(
        """

                            Choose an option:
          0 - Exit 
          1 - Soft Cleaning: Clean spaces and empty columns/rows
          2 - Hard Cleaning: Soft + Clean selected words (on .csv file)
          (Scrubbing included)
          """
        )
        self.option = input("Please select an option: ")
        if self.option == "1": self.option_1()
        elif self.option == "2": self.option_2()
        elif self.option == "0": sys.exit(1)
        else: self.main()
