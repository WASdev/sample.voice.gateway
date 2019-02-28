# Integrating IBM® Voice Gateway with Google Cloud Speech-To-Text

The adapter is a separate Docker container that you deploy together with Voice Gateway and acts as a proxy that sit between Voice Gateway and Google Cloud Speech-To-Text service.

This directory contains the following items:
+ `docker/` - Files to deploy it on Docker Engine with IBM Voice Gateway
+ `kubernetes/bluemix/single-tenant/` - Deployment files for IBM Kubernetes Service

You can find the deployment guides on each of the following links:

+ [Deploying the Speech To Text Adapter on Docker](https://www.ibm.com/support/knowledgecenter/SS4U29/speechadapter_deploydocker.html?view=kc)
+ [Deploying the Speech to Text Adapter to Kubernetes in IBM Cloud Kubernetes Service](https://www.ibm.com/support/knowledgecenter/SS4U29/speechadapter_deploybmix.html?view=kc)


More information can be here: [Integrating third-party speech services](https://www.ibm.com/support/knowledgecenter/SS4U29/speechadapter.html)
