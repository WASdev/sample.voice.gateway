# Samples for using the microservice

Basic samples for understanding and using the Voice Agent Tester microservice. You can quickly start using the microservice by using the `docker-compose.yml` which includes the Agent Tester, a SIP Orchestrator and a Media Relay which are the components for the Caller Voice Gateway, and a CouchDB for the persistence. Just fill in the variables and run `docker-compose up`. If you're going to use the CouchDB service as you persistence then you would have to run a [first time setup](https://docs.couchdb.org/en/master/setup/index.html#setup).

## Microservice samples

The test cases included as samples are designed for testing against a Voice Gateway/Voice Agent running with the demo voice gateway conversation at the [samples repo](https://github.com/WASdev/sample.voice.gateway/blob/master/conversation/sample-conversation-en.json).

Test cases establish the outline of a conversation and are the basic blocks for the service. The tester webhook will validate that the actual conversation matches the conversation established by the test case.

To use them first start the Agent Tester and make sure every necessary variable is filled properly. The test_cases folder contains sample test cases in json format which you could use for using the service. Running a curl command like so

```
curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '@path/to/testcase.json' 'http://localhost:9080/voice-agent-tester/v1/case'
```

You'll get a 201 response back and the id of that newly created test case. Then you would edit a worker from the workers folder and add that id to the cases array.

Workers define the outline of which test cases to run and how many times they will run, how many failures are allowed when running the test cases, and the call definition that will be used when starting calls for the tests. **Important:** make sure that the namespace for test cases and workers match or you'll get an error.

After adding the test case to the worker you can run

```
curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '@path/to/worker.json' 'http://localhost:9080/voice-agent-tester/v1/worker'
```

You'll get a 201 response back and the id of the newly created worker. Then you would use that id to start and manage jobs which are the actual executions of the worker and contain all the data for the running/finished tests. You can start a job by running

```
curl -X POST "http://localhost:9080/voice-agent-tester/v1/worker/{Worker-ID}/job" -H "accept: application/json"
```

This will create a job, return the ID of the newly created job, and start an outbound call following the call definition you defined in the worker. With the ID of the job and the worker you can see the status of the jobs and manage them as you see fit. You can see the job running with its results by running

```
curl -X GET "http://localhost:9080/voice-agent-tester/v1/worker/{Worker-ID}/job/{Job-ID}"
```

To see all the REST endpoints available and their descriptions launch the service and head to http://localhost:9080/openapi/ui which will show the OpenAPI Specification of the service.

## Security Samples

You can quick start using the service by defining the environment variable REST_ADMIN_USERNAME and REST_ADMIN_PASSWORD along with TESTER_WEBHOOK_USERNAME and TESTER_WEBHOOK_PASSWORD. You would use the REST_ADMIN_USERNAME and REST_ADMIN_PASSWORD for authenticating the REST calls and TESTER_WEBHOOK_USERNAME and TESTER_WEBHOOK_PASSWORD will be used for securing the tester webhook endpoints which do the validation. **Important:** Usernames must be different

You can also use your own custom registry for defining user access to the service. The groups are the same for the other Voice Gateway microservices like the Agent Insights service. There are four security groups used by the service: Administrator, Editor, Operator, Viewer. Administrator and Editor have access to all the REST calls of the service. Operator has access to getting test cases and worker, and managing and creating jobs. Viewer only has access to getting test cases, workers, and jobs. The names of the groups are established by the environment variables ROLE_NAME_ADMINISTRATOR, ROLE_NAME_EDITOR, ROLE_NAME_OPERATOR, ROLE_NAME_VIEWER which you can define accordingly to match your registry. You would need to add to your registry the following user

```
<user name="${env.TESTER_WEBHOOK_USERNAME}" password="${env.TESTER_WEBHOOK_PASSWORD}"/>
```

This user is for securing the tester webhook endpoints. It needs to be defined in your registry otherwise no one will have access to the tester webhook. You can see an example of a custom registry in the `security/server-security-incl.xml` directory

Once you have your registry set up, you would need to define the SERVER_REGISTRY_INCLUDE_PATH environment variable as the path to your custom registry. Then start the service and verify that your custom registry is being used

## Deploying on kubernetes

If you wish to deploy the service on a public network with the ability to scale up/down as you wish, look at the kubernetes folder which contains sample deployment scripts and steps for deploying on IBM kubernetes service.