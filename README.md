# League predictions/simulations

Trying to simulate the second half of my team's season...

## Game data

We're getting it from [this FFF API](https://api-dofa.fff.fr/api).

## Tests

Run all tests with:
```sh
make test
```

##  Google Cloud

### Dashboards

- [Main dashboard](https://console.cloud.google.com/home/dashboard?project=promoracle)
- [Artifact Registry repository](https://console.cloud.google.com/artifacts/docker/promoracle/europe-west9/promoracle?project=promoracle)
- [Cloud Run service](https://console.cloud.google.com/run/detail/europe-west9/promoracle/metrics?project=promoracle)
- [Cloud Storage bucket](https://console.cloud.google.com/storage/browser/promoracle;tab=objects?project=promoracle)]

### Commands

To authenticate:
```sh
gcloud init
```

To configure Docker bits:
```sh
gcloud auth configure-docker europe-west9-docker.pkg.dev
```

To push a locally-built image to the repository:
```sh
docker push europe-west9-docker.pkg.dev/promoracle/promoracle/promoracle:latest
```
