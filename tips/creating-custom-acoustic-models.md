# Creating an Custom Acoustic Model

1. Creating the custom acoustic model

	```bash
	curl -X POST -u "<username>:<password>" --header "Content-Type: application/json" --data "{\"name\": \"Chile Custom Acoustic Model\", \"base_model_name\": \"es-ES_NarrowbandModel\", \"description\": \"Example acoustic model for chilean speakers\" }" "https://stream.watsonplatform.net/speech-to-text/api/v1/acoustic_customizations"
	```
	Returns
	```
	{"customization_id": "081d3630-ba58-11e7-aa4b-41bcd3f6f24d"}
	```
2. Add audio to the custom acoustic model
	```bash
	curl -X POST  -u "<username>:<password>" --header "Content-Type: audio/wav" --data-binary @chevere.wav "https://stream.watsonplatform.net/speech-to-text/api/v1/acoustic_customizations/<customization-id>/audio/chevere"
	```

	You can also upload a zip file containing the audio files - https://console.bluemix.net/docs/services/speech-to-text/acoustic-create.html#addAudio

3. Monitor audio request
	```bash
	curl -X GET -u "<username>:<password>" "https://stream.watsonplatform.net/speech-to-text/api/v1/acoustic_customizations/<customization-id>/audio/chevere"
	```

4. Train the model

	For this you require at least 30 minutes of audio. To align the custom acoustic model with a language model you can define the customization_Id of the custom language model as a query parameter: 'customization_id'
	```
	curl -X POST -u "<username>:<password>" "https://stream.watsonplatform.net/speech-to-text/api/v1/acoustic_customizations/<customization-id>/train?customization_id=<custom-language-model-id>"
	```
5. Monitor training
	```
	curl -X GET -u "<username>:<password>" "https://stream.watsonplatform.net/speech-to-text/api/v1/acoustic_customizations/<customization-id>
	```
	You will get a response similar to this:
	```json
	{
	"customization_id": "74f4807e-b5ff-4866-824e-6bba1a84fe96",
	"created": "2016-06-01T18:42:25.324Z",
	"language": "en-US",
	"owner": "297cfd08-330a-22ba-93ce-1a73f454dd98",
	"name": "Example model",
	"description": "Example custom acoustic model",
	"base_model_name": "en-US_BroadbandModel",
	"status": "training",
	"progress": 0
	}
	```

#### References

Creating a custom acoustic model - https://console.bluemix.net/docs/services/speech-to-text/acoustic-create.html#acoustic
