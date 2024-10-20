# Usar la imagen oficial de Ubuntu como base
FROM ubuntu:20.04

# Configurar variables de entorno para evitar preguntas interactivas en la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Actualizar los repositorios e instalar Python 3
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && apt-get clean

# Crear un directorio de trabajo
WORKDIR /workspace

# Copiar la carpeta local `scripts` en el directorio `/workspace` del contenedor
ADD ./scripts /workspace/scripts

# Copiar el archivo archive.pdf.gpg en el directorio de trabajo
ADD ./archive.pdf.gpg /workspace/archive.pdf.gpg

# Establecer Python como el comando por defecto
CMD ["/bin/bash"]

