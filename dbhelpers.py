import unicodedata
import pandas as pd
from db import DB
from report import Report
import sys

class DbHelpers:
    def __init__(self,file_path):
        self.db = DB(file_path)
        self.report = Report(self.db.name)
        self.palabras_path = "words_to_delete.csv"

    def clean_excel_file(self):
        df = self.db.db
        # Delete empty columns
        start_columns = df.shape[1]  # number of columns before
        df = df.dropna(axis=1, how="all")
        end_columns = df.shape[1]  # number of columns after
        columns_removed = start_columns - end_columns
        self.report.update_report("empty_column", columns_removed)

        # Delete empty rows
        start_rows = df.shape[0]  # number of rows before
        df = df.dropna(axis=0, how="all")
        end_rows = df.shape[0]  # number of rows after
        rows_removed = start_rows - end_rows
        self.report.update_report("empty_row", rows_removed)

        # Drop duplicates
        start_rows_after_dropna = end_rows
        df = df.drop_duplicates()
        end_rows_after_drop_duplicates = df.shape[0]
        duplicates_removed = start_rows_after_dropna - end_rows_after_drop_duplicates
        self.report.update_report("duplicated", duplicates_removed)

        # Clean spaces on text columns
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].str.strip()
        self.db.db = df
        return df

    def remove_accent(self, texto):
        if isinstance(texto, str):
            return "".join(
                c
                for c in unicodedata.normalize("NFD", texto)
                if unicodedata.category(c) != "Mn"
            )
        return texto

    def load_words_to_remove(self):
        try:
            df = pd.read_csv(self.palabras_path, header=None)

            # DataFrame to NumPy
            data_array = df.to_numpy()
            if data_array.size == 0:
                return None
            # Flatten array
            data_array = data_array.flatten()
            return data_array
        except FileNotFoundError:
            raise FileNotFoundError(f"El archivo {self.palabras_path} no fue encontrado.")
        except Exception as e:
            raise Exception(f"Ocurrió un error al leer el archivo: {e}")

    def filter_by_words(self):
        words_to_delete = self.load_words_to_remove()
        if words_to_delete is None:
            print("Words not found.")
            sys.exit(1)

        total_rows = len(self.db.db)

        col_to_filter = self.db.db.columns[0] if self.db.db.columns.size > 0 else None
        if col_to_filter is None:
            return "No columns to filter."

        # Normalize cols to delete accents
        self.db.db["temp"] = self.db.db[col_to_filter].apply(self.remove_accent)

        patron = "|".join(words_to_delete)

        # Remove rows that contain the words (ignoring caps and accents)
        df_filtered = self.db.db[~self.db.db["temp"].str.contains(patron, case=False, na=False)]

        # Delete temp col
        df_filtered = df_filtered.drop(columns=["temp"])
        filtered_row = len(df_filtered)

        self.report.update_report("filtered_row", total_rows - filtered_row)

        return df_filtered


