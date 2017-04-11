# IBM&reg; Voice Gateway quick start for bluemix
-------------------
This directory contains bash script files need to quickly deploy a voice gateway to IBM Containers on Bluemix. To see instructions on how to use these scripts go here:

[Deploying to IBM Containers on Bluemix](https://www.ibm.com/support/knowledgecenter/SS4U29/deploybmix.html)

The scripts work with the following CLI versions:

Bluemix CLI (`bx`): `0.5.2+8261395`

IBM Containers Plugin Version (`bx ic`): `1.0.0`

**Note**: Due to a recent change in the Bluemix CLI for IBM Containers we are using timers to wait on the creation of the Voice Gateway containers. These timers can be changed in the `deploy.sh` script on the `sleep` bash commands.
