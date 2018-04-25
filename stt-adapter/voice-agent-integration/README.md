

## Integration with Voice Agent

You can run the Voice Gatway Speech To Text adapter with Google Speech by deploying it to a Kubernetes cluster in IBM Cloud Container Service.

## Before you begin

- Clone or download the [sample.voice.gateway repository](https://github.com/WASdev/sample.voice.gateway) on GitHub. This repository contains sample files for deploying Voice Gateway, such as a Kubernetes deployment file and Calico network policy.

- In IBM Cloud, create a [Kubernetes cluster](https://console.bluemix.net/containers-kubernetes/launch) in IBM Cloud Container Service. For more information about setting up your cluster, see the [IBM Cloud Container Service documentation](https://console.bluemix.net/docs/containers/cs_clusters.html)


## Deploying the Voice Gateway Speech To Text Adapter on a Kubernetes cluster in IBM Cloud

1. Configure the following CLI tools so that you can access your Kubernetes cluster on IBM Cloud through the command line.

    1. [Install the IBM Cloud CLI](https://console.bluemix.net/docs/containers/cs_cli_install.html#cs_cli_install), which is required to interact with IBM Cloud Container Service from the command line.

    1. [Install the IBM Cloud Container Service plug-in (bx cs) and Kubernetes CLI.](https://console.bluemix.net/docs/containers/cs_cli_install.html#cs_cli_install)

        The IBM Cloud Container Service plug-in (bx cs) is needed to manage your Voice Gateway clusters from the command line. The Kubernetes CLI enables you to use native Kubernetes commands to interact with IBM Cloud.

    1. [Configure the IBM Cloud CLI to run kubectl commands.](https://console.bluemix.net/docs/containers/cs_cli_install.html#cs_cli_configure)

        After you configure the CLI, you can run the Kubernetes kubectl commands to work with your Voice Gateway cluster in IBM Cloud.


1. Change to the `stt-adapter/voice-agent-integration` in your local clone of the sample.voice.gateway repository.

1. Create a Kubernetes secret to store the credentials JSON file that you downloaded form your Google Cloud project. Use the `--from-file` option to specify the path to the Google credentials file.

    For example:
    ```
    kubectl create secret generic google-credentials --from-file=/Users/user1/my-google-project-f4b426929b20.json
    ```

1. Mount the Google credentials file to the deployment by specifying the name of the file in the volumes section of the deploy.yaml file,
    For example:

    ```
    ...
      volumes:
      - name: google-credentials
        secret:
          secretName: google-credentials
          items:
            - key: my-google-project-f4b426929b20.json
              path: my-google-project-f4b426929b20.json
    ```

1. Under the `stt-adapter` container, specify the Google credentials file location in the `GOOGLE_APPLICATION_CREDENTIALS environment variable.
  2. For example:
      ```
      spec:
        containers:
        - name: stt-adapter
          ...
          env:
          - name: GOOGLE_APPLICATION_CREDENTIALS
            value: /stt-adapter/credentials/my-google-project-f4b426929b20.json
      ```

1. Deploy your Speech To Text adapter:

    ```
    kubectl create -f deploy.yaml
    ```

1. Run `bx cs workers <name-of-cluster>` and note the public IP as `<public-IP>`.
1. You can validate if the container is listening for requests by using:

    ```
    curl <public-IP>:30082
    ```
    If you see, "Upgrade Required" the STT Adapter is listening for requests from the Voice Gateway.

1. If you want to re-deploy you can delete the deployment:

    ```
      kubectl delete -f deploy.yaml
    ```
    And deploy again:

    ```
      kubectl create -f deploy.yaml
    ```

## Connecting to the Speech To Text Adapter from Voice Agent

1. [Create](https://console.bluemix.net/docs/services/voice-agent/managing.html#managing) or edit an existing voice agent in your Voice Agent instance.
1. Go to the `Speech To Text` section and under the `Service Type` specify an instance of a `Watson Speech To Text` service. Do note this is just a placeholder.
1. Go to your Watson Assistant Workspace, on the first turn which is the "welcome" node and specify a Voice Gateway action to modify the `Speech To Text` configuration for the Voice Gateway, for example: (Note: replace the `<public-IP>` field, when copying and pasting)

```json
{
  "output": {
    "text": {
      "values": [
        "Welcome you are now using a Google Speech engine!"
      ],
      "selection_policy": "sequential"
    },
    "vgwAction": {
      "command": "vgwActSetSTTConfig",
      "parameters": {
        "credentials": {
          "url": "http://<public-IP>:30082"
        },
        "config": {
          "languageCode": "en-US",
          "profanityFilter": true,
          "maxAlternatives": 2
        }
      }
    }
  }
}

```

1. Attempt to make a call and you should now be using the Voice Gateway Speech To Text Adapter with Google Speech.
