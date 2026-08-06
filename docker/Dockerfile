#Descarga de la imagen de python oficial
FROM python:3.14

#Creación del directorio de trabajo
WORKDIR /src

#Copia el archivo con las liberías en el directorio recién creado src
#Solo se copia el archivo de dependencias

COPY ./requirements.txt /src/requirements.txt

#Instala las librerías de python que aparecen en el archivo requriments.txt
#Este archivo se creó previamente a partir de las librerías del entorno virtual
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

#Copia del código del proyecto
COPY ./app /src/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
