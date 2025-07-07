.PHONY: build run stop clean publish

IMAGE_NAME := microservice
IMAGE_TAG ?= 0.1.0

build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

run:
	docker run \
		-p 80:80 \
		--name $(IMAGE_NAME) \
		$(IMAGE_NAME):$(IMAGE_TAG)

it:
	docker run \
		-p 80:80 \
		--interactive \
		--tty \
		--name $(IMAGE_NAME) \
		$(IMAGE_NAME):$(IMAGE_TAG)

bash:
	docker exec -it $(IMAGE_NAME) sh

stop:
	docker stop $(IMAGE_NAME) && docker rm $(IMAGE_NAME)

publish:
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)
	docker push $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)

copy:
	docker cp $(IMAGE_NAME):/app/app.db ./app2.db

test:
	python -m pytest

clear:
	docker container rm $(IMAGE_NAME)
	docker image rm $(IMAGE_NAME):$(IMAGE_TAG)