import gnupg
import itertools
import string
from multiprocessing import Process, Event, Manager
import os  # Para manejar la afinidad de los procesos (CPU affinity)

# Crear una instancia de GPG
gpg = gnupg.GPG()

# Archivo a descifrar
gpg_file = "archive.pdf.gpg"

# Todas las letras minúsculas
chars = string.ascii_lowercase

# Número de procesos a usar
NUM_PROCESSES = 4  # Cambia esto según el número de núcleos disponibles

# Tamaño del lote de contraseñas para que cada proceso las pruebe
BATCH_SIZE = 100

def set_affinity(core_id):
    """Establecer la afinidad de CPU (núcleo) para este proceso."""
    try:
        # Fijar el proceso al núcleo core_id
        os.sched_setaffinity(0, {core_id})  # El 0 indica que estamos fijando la afinidad del proceso actual
        print(f"Proceso {os.getpid()} asignado al núcleo {core_id}")
    except AttributeError:
        print("La afinidad de CPU no está soportada en este sistema operativo.")

def try_decrypt(passphrase, password_found_event, shared_result):
    if password_found_event.is_set():
        return False  # Si ya se encontró la contraseña, el proceso se detiene

    try:
        # Feedback de la contraseña que se está probando
        print(f"Proceso {os.getpid()} probando contraseña: {passphrase}")

        # Abrir el archivo cifrado
        with open(gpg_file, "rb") as f:
            # Intentar descifrar el archivo
            result = gpg.decrypt_file(f, passphrase=passphrase)

            # Verificar si la contraseña es correcta
            if result.ok:
                print(f"¡Contraseña encontrada!: {passphrase}")
                shared_result.append(passphrase)  # Guardar la contraseña encontrada
                password_found_event.set()  # Marcar el evento como "encontrado"
                return True
            else:
                return False
    except Exception as e:
        print(f"Error al intentar descifrar con {passphrase}: {e}")
        return False

def brute_force_process_worker(all_passwords, core_id, password_found_event, shared_result):
    # Establecer la afinidad del proceso a un núcleo específico
    set_affinity(core_id)

    # Cada proceso obtiene su propio lote de contraseñas para probar
    for passphrase in all_passwords:
        passphrase = ''.join(passphrase)
        if try_decrypt(passphrase, password_found_event, shared_result):
            return  # Si encuentra la contraseña, salir del bucle
        if password_found_event.is_set():
            break  # Si otro proceso ya encontró la contraseña, salir

# Ataque de fuerza bruta generando todas las combinaciones posibles
def brute_force_attack():
    manager = Manager()
    password_found_event = manager.Event()  # Evento compartido entre los procesos
    shared_result = manager.list()  # Lista compartida para guardar la contraseña encontrada

    # Empezar probando contraseñas de longitud 1, luego 2, y así sucesivamente
    for length in range(1, 5):  # Cambia '4' por un número mayor si necesitas probar más longitud de contraseñas
        print(f"Probando contraseñas de longitud {length}...")

        # Generar todas las combinaciones posibles de la longitud actual
        all_passwords = list(itertools.product(chars, repeat=length))

        # Dividir las contraseñas entre los procesos
        total_passwords = len(all_passwords)
        passwords_per_process = total_passwords // NUM_PROCESSES
        processes = []

        for i in range(NUM_PROCESSES):
            # Asignar a cada proceso un rango único de contraseñas
            start_index = i * passwords_per_process
            # Último proceso toma lo que quede
            if i == NUM_PROCESSES - 1:
                process_passwords = all_passwords[start_index:]
            else:
                end_index = (i + 1) * passwords_per_process
                process_passwords = all_passwords[start_index:end_index]

            # Crear y lanzar el proceso
            core_id = i  # Asignar este proceso al núcleo i
            process = Process(target=brute_force_process_worker, args=(process_passwords, core_id, password_found_event, shared_result))
            processes.append(process)
            process.start()

        # Esperar a que todos los procesos terminen
        for process in processes:
            process.join()

        # Si la contraseña fue encontrada, detener el ataque
        if shared_result:
            print(f"¡Contraseña encontrada por uno de los procesos!: {shared_result[0]}")
            break

# Iniciar el ataque de fuerza bruta multiproceso con afinidad de CPU
brute_force_attack()
