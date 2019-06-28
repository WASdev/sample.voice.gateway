# Samples for deploying and scaling on kubernetes

This directory contains various samples for scaling the Agent Tester microservice and the Caller Voice Gateway for driving batch jobs with many concurrent jobs.

## Prerequisites

You must have an account for Watson Services Text to Speech and Speech to Text and also a kubernetes cluster service. Configure the following CLI tools so that you can access your Kubernetes cluster on IBM Cloud through the command line

1. [Install the IBM Cloud CLI](https://console.bluemix.net/docs/containers/cs_cli_install.html#cs_cli_install), which is required to interact with the IBM Cloud from the command line.
2. [Install the IBM Cloud Kubernetes plug-in (ibmcloud ks) and Kubernetes CLI](https://console.bluemix.net/docs/containers/cs_cli_install.html#cs_cli_install). The Kubernetes CLI enables you to use native Kubernetes commands to interact with your cluster.

3. [Configure the IBM Cloud CLI to run `kubectl` commands](https://console.bluemix.net/docs/containers/cs_cli_install.html#cs_cli_configure). After you configure the CLI, you can run the Kubernetes `kubectl` commands to work with your cluster.

4. [Install and configure the Calico CLI](https://console.bluemix.net/docs/containers/cs_network_policy.html#cli_install) so that you can use the `calicoctl` commands to change the default network policies. Network policies specify the network traffic that you want to allow or block to and from a pod in a cluster.

## Steps for deploying

1. Setup the endpoints that you will test against to receive multiple concurrent calls. If you're using a twilio SIP trunk edit the termination so that its able to manage more than 1 Call per Second (CPS) to the number of concurrent calls you wish to run (THIS COULD CHANGE). If you're running against a K8 or local deployment make sure its able to handle all the calls you will concurrently run. If you're running against a Voice Agent make sure that the maximum concurrent connections it can handle is sufficient.

2. Setup your cluster and set up the  with the number of nodes you deem necessary depending on the amount of concurrent calls you wish to place. Depending on the resources given to the node is the amount of calls it can handle. In a normal testing environment it was found that a node with 2 CPU cores and 4 GB RAM could handle arround 70 calls and when the CPU's where doubled the amount of calls it could handle was doubled too howerver you should experiment and adapt as you deem necessary.

3. Create all the necessary credentials that will be used. Edit the `caller_and_tester/creds.yml` to match all your credentials for deploying. Then in a terminal instance run `kubectl apply -f creds.yml` which will create the credentials as a secret in you cluster. If you wish, you can also deploy a couchdb instance in which all the data will be stored. You can find samples for deploying a single couchdb node in the `couchdb` directory. If so, edit the `couchdb/couchdb-secret.yml` with what you desire and run `kubectl apply -f couchdb/couchdb-secret.yml`.

4. Create all the necessary services for app networking. The two services used for exposing the microservice and the outbound calls are `caller_and_tester/agent_tester_service.yml` and `caller_and_tester/outbound_call_service.yml`. In a terminal instance run:

    ```
    kubectl apply -f caller_and_tester/agent_tester_service.yml
    kubectl apply -f caller_and_tester/outbound_call_service.yml
    ```

    If you will be deploying a couchdb instance in the cluster also run `kubectl apply -f couchdb/couchdb-service.yml`. The service is currently set as NodePort for you to set it up once your deployment is in place. Then you should either modify it to be internal or take the necessary steps for securing your database.

5. Create all the deployments. Change anything you wish to change from the deployments in the `caller_and_tester` directory and then run:

    ```
    kubectl apply -f caller_and_tester/agent_tester_deployment.yml
    kubectl apply -f caller_and_tester/caller_deployment.yml
    ```

    For deploying the couchdb instance first run `kubectl apply -f couchdb/couchdb-persistence-volume.yml` which will create a persistent volume used to store the data. Then run `kubectl apply -f couchdb/couchdb-single-stateful-set.yml` which will deploy couchdb to the cluster. Since its a first time run you would need to configure the couchdb instance as a single node. Details [here](https://docs.couchdb.org/en/master/setup/single-node.html) with the IP being from a worker running `ibmcloud ks workers <CLUSTER_NAME>` and the port given by `kubectl get services`. Removing this stateful set also removes all the persistence it has so you may want to back up the data, however if a pod fails then the data is not lost.

6. Apply the calico network policy in the `caller_and_tester` directory. Run `calicoctl apply -f caller_and_tester/calico-v3.yml`

7. Now everything is ready for starting concurrent calls! Give it a try. You can scale up the `caller_deployment` to as many as the number of nodes in your cluster and you can scale up the `agent_tester_deployment` as you deem necessary but if so you would need to turn of caching in the microservice as stated in the deployment sample. To scale run `kubectl scale deployment <NAME_OF_DEPLOYMENT> --replicas=<NUMBER_OF_REPLICAS>`
