import pandas as pd
import unicodedata
import os
import sys


def eliminar_tildes(texto):
    if isinstance(texto, str):
        return "".join(
            c
            for c in unicodedata.normalize("NFD", texto)
            if unicodedata.category(c) != "Mn"
        )
    return texto


def import_excel_file(file):
    # Leer archivo Excel
    try:
        df = pd.read_excel(file)
        if df.empty:
            return "El archivo está vacío."
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo {file} no fue encontrado.")
    except Exception as e:
        raise Exception(f"Ocurrió un error al leer el archivo: {e}")


def save_excel_file(df, file_path):
    # Guardar archivo limpio
    name = file_path.split("/")[-1]
    newName = "healthy_" + name
    directory = "./result/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    msg = f"Archivo limpio guardado como {newName} en: {directory}"
    df.to_excel(directory + newName, index=False)
    return msg


def clean_excel_file(df):

    # Eliminar columnas vacías
    df = df.dropna(axis=1, how="all")
    # Eliminar filas vacías
    df = df.dropna(axis=0, how="all")

    df = df.drop_duplicates()

    # Limpiar espacios en columnas de texto
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()
    return df


def hard_clean_excel_file(df):
    df = clean_excel_file(df)

    columna_a_filtrar = df.columns[0] if df.columns.size > 0 else None
    if columna_a_filtrar is None:
        return "No hay columnas para filtrar."

    # Normalizar columna para eliminar tildes
    df["col_sin_tilde"] = df[columna_a_filtrar].apply(eliminar_tildes)

    palabras_eliminar = load_words_to_remove("palabras_a_eliminar.csv")
    print(palabras_eliminar)
    if palabras_eliminar is None:
        print("No hay palabras a eliminar.")
        sys.exit(1)

    patron = "|".join(palabras_eliminar)

    # Filtrar filas que NO contienen esas palabras (ignorando mayúsculas y tildes)
    df_filtrado = df[~df["col_sin_tilde"].str.contains(patron, case=False, na=False)]

    # Eliminar columna auxiliar
    df_filtrado = df_filtrado.drop(columns=["col_sin_tilde"])

    return df_filtrado


def load_words_to_remove(file_path):
    try:
        df = pd.read_csv(file_path, header=None)

        # Convertir el DataFrame a un array de NumPy
        data_array = df.to_numpy()
        if data_array.size == 0:
            return None
        # Aplanar el array si es necesario
        data_array = data_array.flatten()
        return data_array
    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo {file_path} no fue encontrado.")
    except Exception as e:
        raise Exception(f"Ocurrió un error al leer el archivo: {e}")
