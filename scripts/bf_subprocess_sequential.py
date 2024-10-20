import subprocess
import itertools
import string

gpg_file = "test.txt.gpg"

# Todas las letras minúsculas
chars = string.ascii_lowercase

def try_decrypt(passphrase):
    try:
        command = ["gpg", "--batch", "--yes", "--passphrase", passphrase, "--decrypt", gpg_file]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            print(f"¡Contraseña encontrada!: {passphrase}")
            return True
        else:
            return False
    except Exception as e:
        print(f"Error al intentar descifrar con {passphrase}: {e}")
        return False

# Ataque de fuerza bruta generando todas las combinaciones posibles
def brute_force_attack():
    # Empezar por contraseñas de longitud 1, luego 2, 3, etc.
    for length in range(1, 10):
        for passphrase in itertools.product(chars, repeat=length):
            passphrase = ''.join(passphrase)
            print(f"Probando contraseña: {passphrase}")
            if try_decrypt(passphrase):
                return

# Iniciar el ataque de fuerza bruta
brute_force_attack()
