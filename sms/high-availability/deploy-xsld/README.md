## Explanation and steps
1. Download or clone the samples repository if this has not performed previously
    ```
    git clone https://github.com/WASdev/sample.voice.gateway
    cd sms/high-availability
    ```
1. Set the permission of the scripts to be executable:
    ```
    chmod +x *.sh
    ```
1. Define a password for the default XSLD Admin User "xsadmin" in the `deploy.config` file in the `xsadminPass` variable, this defaults to `vgwAdmin4xs!`.

1. Deploy Voice Gateway XSLD on your Kubernetes cluster,
    This step will deploy the XSLD image on specified number of nodes/pods
    ```
    ./deploy-xsld-image.sh
    ```

1. Start containers on XSLD pods.
    This step will verify the vgw-xsld container on the nodes/pods have started
    ```
    ./verify-xsld-pods-started.sh
    ```
1. Verify the containers are listening for requests and/or check the xsld dashboard
    ```
    ./verify-xsld-pods-listening.sh
    ```
    Check the XSLD dashboard by accessing `https://<ip-address>:9443/wxsui`, you can obtain the IP Addresses/hostnames by running the following command

    ```bash
    kubectl get pods -o wide -l service=vgw-xsld --no-headers | awk '{ print $6}'
    ```

1. Join the XSLD instances to enable cache replication and failover.
    ```bash
    ./join-xsld-members.sh
    ```
    or Join the members using XSLD dashboard by accessing `https://<ip-address>:9443/wxsui`


1. Setup XSLD to be used with SMS Gateway
    ```bash
    ./deploy-smsgw-grid-application.sh
    ```

1. Get the xsld catalog endpoints which will be required to deploy SMS Gateway instance
    ```bash
    ./get-catalog-endpoints-for-smsgw.sh
    ```
