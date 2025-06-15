import os
from abc import ABC as abc

class Report:
    def __init__(self, file_name):
        self.file_path = "./result/report.txt"
        self.directory = "./result/"
        self.file_name = file_name
        self.report_data = ReportData()
        self.result = ""

    def update_report(self,prop,param):
        if not hasattr(self.report_data, prop):
            print("No se encontró la propiedad")
        else:
            current_value = getattr(self.report_data, prop)
            setattr(self.report_data, prop, current_value + param)
            self.create_report()
            self.save_report()

    def create_report(self):
        self.result = f"""
        
File: {self.file_name}
    
    Result:
        Empty rows: {self.report_data.empty_row}
        Empty cols: {self.report_data.empty_column}
        Duplicated: {self.report_data.duplicated}
        Empty number, website and email rows: {self.report_data.no_contact_row}
        CSV coincidence rows: {self.report_data.filtered_row}
                
    Process exited after: {self.report_data.time}
                
"""
        return self.result

    def read_report(self):
        print(self.result)
        return

    def save_report(self):
        # Guardar archivo limpio
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        with open(self.file_path, "w") as f:
            f.write(self.create_report())

        return f"Reporte guardado como report.txt en: {self.directory}"

class ReportData:
    def __init__(self):
        self.empty_row = 0
        self.empty_column = 0
        self.duplicated = 0
        self.filtered_row = 0
        self.no_contact_row = 0
        self.time = 0
