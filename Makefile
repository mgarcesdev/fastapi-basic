install:
	pip install -r requirements.txt

# Nombre de la imagen
IMAGE_NAME=fastapi-basic
DOCKER_USER=mgarcesdev
TAG=latest

# Comando para construir la imagen
build:
	docker-compose build

# Comando para ejecutar los contenedores en segundo plano
up:
	docker-compose up -d

# Comando para detener los contenedores y eliminar los recursos (contenedores, redes, etc.)
down:
	docker-compose down

# Comando para construir la imagen y ejecutar el contenedor (en un solo paso)
build-up: build up

# Comando para ver los logs de la aplicación
logs:
	docker-compose logs -f fastapi

# Comando para eliminar todas las imágenes y contenedores no utilizados
prune:
	docker system prune -a --volumes --force

# Comando para acceder al contenedor de la aplicación (para depuración)
exec:
	docker-compose exec fastapi bash

# Comando para etiquetar la imagen para Docker Hub
tag:
	docker tag $(IMAGE_NAME) $(DOCKER_USER)/$(IMAGE_NAME):$(TAG)

# Comando para subir la imagen a Docker Hub
push: tag
	docker push $(DOCKER_USER)/$(IMAGE_NAME):$(TAG)

# Comando para construir, etiquetar y subir la imagen a Docker Hub
build-push: build tag push