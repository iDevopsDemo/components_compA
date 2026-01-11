# DataProvider (comp-a)

This component constantly generates messages and send these messages to a MQTT broker.

## How to use

Just start the docker container with:

```sh
docker run --rm --name dataprovider ghcr.io/idevopsdemo/comp-a
```

Deploy via Helm

(Optional) In case of private registry usage, login to the registry first:

```sh
helm registry login -u myuser oci://ghcr.io/idevopsdemo/charts/comp-a
```

```sh
helm install -n my-namespace comp-a oci://ghcr.io/idevopsdemo/charts/comp-a

#in order to deploy pre-release version use
helm install -n my-namespace --devel comp-a oci://ghcr.io/idevopsdemo/charts/comp-a
```

### Optional Parameters

The following environment variables are available to adjust the behavior:

* **DATAPROVIDER_TOPIC** allows to overwrite the default topic default: `sample/message`
* **QCLIENT_BROKER_HOST** ip address of the mqtt broker to use default: 127.0.0.1
* **QCLIENT_BROKER_PORT** port of mqtt broker to use default: 1883

```sh
docker run --rm --name dataprovider -e DATAPROVIDER_TOPIC='my/message/is/better' dataprovider ghcr.io/idevopsdemo/comp-a
```

### Build Test Trigger

123456
