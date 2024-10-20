import gnupg
import itertools
import string

# Crear una instancia de GPG
gpg = gnupg.GPG()

# Archivo a descifrar
gpg_file = "test.txt.gpg"

# Todas las letras minúsculas
chars = string.ascii_lowercase

def try_decrypt(passphrase):
    try:
        # Abrir el archivo cifrado
        with open(gpg_file, "rb") as f:
            # Intentar descifrar el archivo
            result = gpg.decrypt_file(f, passphrase=passphrase)

            # Verificar si la contraseña es correcta
            if result.ok:
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
    for length in range(1, 10):  # Puedes aumentar el rango según sea necesario
        for passphrase in itertools.product(chars, repeat=length):
            passphrase = ''.join(passphrase)
            print(f"Probando contraseña: {passphrase}")
            if try_decrypt(passphrase):
                return

# Iniciar el ataque de fuerza bruta
brute_force_attack()

