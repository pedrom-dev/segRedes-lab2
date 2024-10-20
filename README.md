# Seguridad en Redes - Laboratorio 2

Este repositorio contiene todos los archivos y scripts utilizados para realizar el ataque de fuerza bruta sobre un archivo cifrado con GPG como parte de la práctica 2 del laboratorio de Seguridad en Redes. A continuación se describe el contenido de cada archivo.

## Archivos del repositorio

- **`Memoria.pdf`**: Documento que contiene la memoria completa del proceso realizado, donde se explican los pasos, los enfoques probados, y los resultados obtenidos durante el ataque de fuerza bruta.

- **`scripts/`**: Carpeta que contiene todos los scripts probados durante la práctica. Cada script representa un enfoque diferente para realizar el ataque de fuerza bruta, incluyendo enfoques secuenciales, multihilo y multiproceso. Además, se incluye el archivo `test.txt.gpg` utilizado en algunas de las pruebas.

- **`results.txt`**: Archivo que contiene los resultados de los tiempos de ejecución de cada uno de los scripts cuando fueron probados dentro de un contenedor Docker. Los resultados muestran la eficiencia de cada enfoque.

- **`Dockerfile`**: Archivo utilizado para desplegar el entorno Docker controlado en el que se realizaron las pruebas de ejecución de los scripts. Este Dockerfile configura un entorno con las dependencias necesarias y asigna los recursos para ejecutar los scripts de manera uniforme.

- **`archive.pdf.gpg`**: Archivo cifrado proporcionado como parte de la práctica. El objetivo del ataque de fuerza bruta es encontrar la passphrase que permite desencriptar este archivo.

- **`bf_multiprocessing_cpu_affinity_used.py`**: Script final utilizado para desencriptar el archivo **`archive.pdf.gpg`**. Este script emplea el enfoque de **multiprocessing con afinidad de CPU** para realizar el ataque de fuerza bruta de manera más eficiente.

- **`README.md`**: Este archivo, que describe el contenido del repositorio y explica brevemente el propósito de cada archivo.

## Ejecución en Docker

Para ejecutar los scripts dentro de un contenedor Docker controlado, sigue estos pasos:

1. **Construir la imagen de Docker**:
   ```bash
   docker build -t fuerza_bruta_gpg .

2. **Ejecutar el contenedor con 4 núcleos de CPU**:
    ```bash
    docker run -it --cpus="4" fuerza_bruta_gpg
