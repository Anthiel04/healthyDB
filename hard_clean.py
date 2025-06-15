import pandas as pd
import sys
from dbhelpers import DbHelpers

class HC:
    def __init__(self, helper):
        self.tools = helper

    def main(self):
        self.tools.clean_excel_file()
        self.tools.filter_by_words()