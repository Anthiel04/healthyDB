from dbhelpers import DbHelpers

class SC:
    def __init__(self, helper):
        self.tools = helper

    def main(self):
        self.tools.clean_excel_file()
