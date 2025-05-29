import sys
import time
import cure


def main():
    # Verifica si se ha proporcionado un argumento
    if len(sys.argv) < 2:
        print("Uso: python main.py <path> profile")
        sys.exit(1)

    # Obtiene el path del archivo desde los argumentos
    file_path = sys.argv[1]

    if len(sys.argv) < 3:
        profile = None
    else:
        # Obtiene el perfil desde los argumentos
        profile = sys.argv[2]

    start = time.time()

    if profile == "hard":
        print(f"Aplicando saneamiento fuerte.")
        try:
            print(f"Procesando el archivo: {file_path}")
            excel = cure.import_excel_file(file_path)
            processed = cure.hard_clean_excel_file(excel)
            cure.save_excel_file(processed, file_path)
            elapsed = time.time()

            print(f"Done in {start - elapsed} seconds")

        except FileNotFoundError:
            print(f"El archivo {file_path} no fue encontrado.")
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            sys.exit(1)
    else:
        print("Aplicando saneamiento básico.")
        try:
            print(f"Procesando el archivo: {file_path}")
            excel = cure.import_excel_file(file_path)
            processed = cure.clean_excel_file(excel)
            cure.save_excel_file(processed, file_path)
            elapsed = time.time()

            print(f"Done in {start - elapsed} seconds")

        except FileNotFoundError:
            print(f"El archivo {file_path} no fue encontrado.")
        except Exception as e:
            print(f"Ocurrió un error: {e}")

    # Intenta abrir y leer el archivo


if __name__ == "__main__":
    main()
