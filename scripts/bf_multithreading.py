import gnupg
import itertools
import string
import threading

# Crear una instancia de GPG
gpg = gnupg.GPG()

# Archivo a descifrar
gpg_file = "test.txt.gpg"

# Todas las letras minúsculas
chars = string.ascii_lowercase

# Número de hilos a usar
NUM_THREADS = 4

# Tamaño del lote de contraseñas para que cada hilo las pruebe
BATCH_SIZE = 100

# Evento para indicar cuándo se ha encontrado la contraseña
password_found_event = threading.Event()

def try_decrypt(passphrase):
    if password_found_event.is_set():
        return False  # Si ya se encontró la contraseña, el hilo se detiene

    try:
        # Feedback de la contraseña que se está probando
        print(f"Hilo {threading.current_thread().name} probando contraseña: {passphrase}")

        # Abrir el archivo cifrado
        with open(gpg_file, "rb") as f:
            # Intentar descifrar el archivo
            result = gpg.decrypt_file(f, passphrase=passphrase)

            # Verificar si la contraseña es correcta
            if result.ok:
                print(f"¡Contraseña encontrada!: {passphrase}")
                # Marcar el evento como "encontrado"
                password_found_event.set()
                return True
            else:
                return False
    except Exception as e:
        print(f"Error al intentar descifrar con {passphrase}: {e}")
        return False

def brute_force_thread_worker(all_passwords):
    # Cada hilo obtiene su propio lote de contraseñas para probar
    for passphrase in all_passwords:
        passphrase = ''.join(passphrase)
        if try_decrypt(passphrase):
            return  # Si encuentra la contraseña, sale del bucle
        if password_found_event.is_set():
            break  # Si otro hilo ya encontró la contraseña, salir

# Ataque de fuerza bruta generando todas las combinaciones posibles
def brute_force_attack():
    # Empezar probando contraseñas de longitud 1, luego 2, y así sucesivamente
    for length in range(1, 4):  # Cambia '4' por un número mayor si necesitas probar más longitud de contraseñas
        print(f"Probando contraseñas de longitud {length}...")

        # Generar todas las combinaciones posibles de la longitud actual
        all_passwords = list(itertools.product(chars, repeat=length))

        # Dividir las contraseñas entre los hilos
        total_passwords = len(all_passwords)
        passwords_per_thread = total_passwords // NUM_THREADS
        threads = []

        for i in range(NUM_THREADS):
            # Asignar a cada hilo un rango único de contraseñas
            start_index = i * passwords_per_thread
            # Último hilo toma lo que quede
            if i == NUM_THREADS - 1:
                thread_passwords = all_passwords[start_index:]
            else:
                end_index = (i + 1) * passwords_per_thread
                thread_passwords = all_passwords[start_index:end_index]

            # Crear y lanzar el hilo
            thread = threading.Thread(target=brute_force_thread_worker, args=(thread_passwords,))
            threads.append(thread)
            thread.start()

        # Esperar a que todos los hilos terminen
        for thread in threads:
            thread.join()

# Iniciar el ataque de fuerza bruta multihilo
brute_force_attack()

