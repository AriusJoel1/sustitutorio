import os

ruta_base = os.path.abspath(".")
nombre_script = os.path.basename(__file__)
archivo_salida = os.path.join(ruta_base, "proyecto_resumen.txt")

with open(archivo_salida, "w", encoding="utf-8") as salida:

    salida.write("ESTRUCTURA DEL PROYECTO\n")
    for root, dirs, files in os.walk(ruta_base):
        nivel = root.replace(ruta_base, "").count(os.sep)
        indent = "  " * nivel
        carpeta = os.path.basename(root)
        salida.write(f"{indent}{carpeta}/\n")
        for f in files:
            if f == nombre_script:
                continue
            salida.write(f"{indent}  {f}\n")

    salida.write("\nCONTENIDO DE ARCHIVOS\n")
    for root, dirs, files in os.walk(ruta_base):
        for f in files:
            if f == nombre_script:
                continue
            ruta_archivo = os.path.join(root, f)
            salida.write(f"\n--- {os.path.relpath(ruta_archivo, ruta_base)} ---\n")
            try:
                with open(ruta_archivo, "r", encoding="utf-8") as file:
                    contenido = file.read()
                    salida.write(contenido + "\n")
            except Exception as e:
                salida.write(f"[No se pudo leer el archivo: {e}]\n")
