# DataProvider (comp-a)

This component constantly generates messages and send these messages to a MQTT broker.

## How to use

Just start the docker container with:

```sh
docker run --rm --name dataprovider docker.artifactory.mydevops.info/xo-sample/comp-a
```

Deploy via Helm

```sh
helm repo add xo-sample https://artifactory.mydevops.info/artifactory/helm-xo-sample
helm repo update

helm install -n xo-sample comp-a xo-sample/comp-a

#in order to deploy pre-release version use
helm install -n xo-sample --devel comp-a xo-sample/comp-a
```

### Optional Parameters

The following environment variables are available to adjust the behavior:

* **DATAPROVIDER_TOPIC** allows to overwrite the default topic default: `sample/message`
* **QCLIENT_BROKER_HOST** ip address of the mqtt broker to use default: 127.0.0.1
* **QCLIENT_BROKER_PORT** port of mqtt broker to use default: 1883

```sh
docker run --rm --name dataprovider -e DATAPROVIDER_TOPIC='my/message/is/better' docker.artifactory.mydevops.info/xo-sample/comp-a
```

### Build Test Trigger

1234567
