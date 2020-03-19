.PHONY: build docker test clean prepare update

GO=CGO_ENABLED=0 GO111MODULE=on go

MICROSERVICES=cmd/ev-charger-device-service
.PHONY: $(MICROSERVICES)


GOFLAGS=-ldflags "-X github.com/CamusEnergy/kinney/controller/ev-charger-device-service.Version=$(VERSION)"

build: $(MICROSERVICES)

cmd/ev-charger-device-service:
	$(GO) build $(GOFLAGS) -o $@ ./cmd

docker:
	docker build . \
		--build-arg http_proxy=$(HTTP_PROXY) \
		--build-arg https_proxy=$(HTTPS_PROXY) \
		--build-arg no_proxy=$(NO_PROXY) \
		-t ev-charger-device-service
# test:
# 	go test -coverprofile=coverage.out ./...
# 	go vet ./...

# check-lint:
# 	which golint || (go get -u golang.org/x/lint/golint)

# lint: check-lint
# 	golint ./...

# coveragehtml:
# 	go tool cover -html=coverage.out -o coverage.html

# format:
# 	gofmt -l .
# 	[ "`gofmt -l .`" = "" ]

update:
	$(GO) mod download

clean:
	rm -f $(MICROSERVICES)