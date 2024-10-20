import subprocess
import threading

# Archivo GPG que vamos a descifrar
gpg_file = "archive.pdf.gpg"
# Archivo de salida después de descifrar
output_file = "archive.pdf"
# Archivo de diccionario (en este caso rockyou.txt)
wordlist_file = "rockyou.txt"

# Número de hilos a usar
num_threads = 8

# Bandera para detener todos los hilos si se encuentra la clave correcta
found = False

# Bloqueo para asegurar el acceso exclusivo a la variable 'found'
lock = threading.Lock()

# Función que intenta descifrar el archivo con la frase de paso dada
def try_decrypt(passphrase):
    global found
    with lock:
        if found:
            return True
    
    print(f"Probando contraseña: {passphrase.strip()}")  # Añadir depuración para ver las contraseñas probadas
    
    try:
        # Comando gpg para descifrar
        command = ["gpg", "--batch", "--yes", "--passphrase", passphrase.strip(), "--output", output_file, "--decrypt", gpg_file]
        
        # Ejecutar el comando gpg
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Si no hay errores, significa que la clave es correcta
        if result.returncode == 0:
            with lock:
                print(f"¡Clave encontrada!: {passphrase.strip()}")
                found = True
            return True
        else:
            return False

    except Exception as e:
        print(f"Error al intentar descifrar con {passphrase.strip()}: {e}")
        return False

# Función que procesa una porción del archivo de diccionario
def dictionary_attack_thread(start_index, step):
    global found
    try:
        with open(wordlist_file, "r", encoding="utf-8", errors="ignore") as wordlist:
            for i, passphrase in enumerate(wordlist):
                if i % step == start_index:  # Cada hilo toma una parte del archivo
                    if found:
                        return
                    try_decrypt(passphrase)
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {wordlist_file}")

# Ejecutar el ataque de diccionario utilizando hilos
def dictionary_attack_with_threads():
    threads = []
    
    # Crear y empezar los hilos
    for i in range(num_threads):
        t = threading.Thread(target=dictionary_attack_thread, args=(i, num_threads))
        threads.append(t)
        t.start()
    
    # Esperar a que todos los hilos terminen
    for t in threads:
        t.join()

# Ejecutar el ataque
dictionary_attack_with_threads()

