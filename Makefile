default: docker_k8s_build

.PHONY: ecr_login
ecr_login:
	@$$(aws ecr get-login --no-include-email --region eu-west-1)

.PHONY: docker_build
docker_build:
	@docker build \
		--build-arg VCS_REF=`git rev-parse --short HEAD` \
		--build-arg BUILD_DATE=`date -u +"%Y-%m-%dT%H:%M:%SZ"` \
		--build-arg VERSION=`cat VERSION` \
		-t 268324876595.dkr.ecr.eu-west-1.amazonaws.com/apache-pulsar-grafana-dashboard:`cat VERSION` \
		.

.PHONY: docker_k8s_build
docker_k8s_build:
	@docker build \
		--build-arg VCS_REF=`git rev-parse --short HEAD` \
		--build-arg BUILD_DATE=`date -u +"%Y-%m-%dT%H:%M:%SZ"` \
		--build-arg VERSION=`cat VERSION` \
		-f Dockerfile.kubernetes \
		-t 268324876595.dkr.ecr.eu-west-1.amazonaws.com/apache-pulsar-grafana-dashboard-k8s:`cat VERSION` \
		.

.PHONY: push_image
push_image:
	@docker push 268324876595.dkr.ecr.eu-west-1.amazonaws.com/apache-pulsar-grafana-dashboard-k8s:`cat VERSION`
