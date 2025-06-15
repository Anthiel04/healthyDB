import os
import pandas as pd

class DB:
    def __init__(self,file_path):
        self.file_path = file_path
        self.name = self.file_path.split("/")[-1]
        self.newName = "healthy_" + self.name
        self.directory = "./result/"
        self.db = self.import_excel_file()

    def import_excel_file(self):
        # Read Excel
        try:
            df = pd.read_excel(self.file_path)
            if df.empty:
                return "File is empty."
            return df
        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.file_path} not found.")
        except Exception as e:
            raise Exception(f"Something went wrong: {e}")

    def save_excel_file(self):
        # Save clean file
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.db.to_excel(self.directory + self.newName, index=False)
        return f"Archivo limpio guardado como {self.newName} en: {self.directory}"
