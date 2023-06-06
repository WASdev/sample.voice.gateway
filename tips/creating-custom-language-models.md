# Creating custom language models


1. Create a custom language model:
	```bash
	curl -X POST -u "<username>:<password>" --header "Content-Type: application/json" --data "{\"name\": \"Chile Custom Language Model Example\", \"base_model_name\": \"es-ES_NarrowbandModel\", \"dialect\": \"es-LA\", \"description\": \"Example language model for chilean speakers\" }" "https://stream.watsonplatform.net/speech-to-text/api/v1/customizations"
	```
	Returns:
	{"customization_id": "e4766090-ba51-11e7-be33-99bd3ac8fa93"}


2. Create a corpora - https://console.bluemix.net/docs/services/speech-to-text/language-resource.html#workingCorpora

	For example, create a text file named "sample-phrases.txt" with the following content:

	```text
	vale
	tienda
	horario
	Santiago
	Alameda O'Higgins
	Lomo Santa Lucia
	agarrar onda
	apretar cachete
	al tiro
	cachar
	Espérate un cachito
	```


3.  Add the Corpora to the Language Model
	```bash
	curl -X POST -u "<username>:<password>" --data-binary @sample-phrases.txt "https://stream.watsonplatform.net/speech-to-text/api/v1/customizations/<customization-id>/corpora/sample_phrases"
	```

4. Monitor the corpora request

	```bash
	curl -X GET -u "<username>:<password>" "https://stream.watsonplatform.net/speech-to-text/api/v1/customizations/<customization-id>/corpora/sample_phrases"
	```

	Returns:
	```json
	{
	"out_of_vocabulary_words": 2,
	"total_words": 19,
	"name": "sample_phrases",
	"status": "analyzed"
	}
	```

	The status field has one of the following values:
	analyzed indicates that the service has successfully analyzed the corpus.
	being_processed indicates that the service is still analyzing the corpus.
	undetermined indicates that the service encountered an error while processing the corpus

5. Adding words to the custom language model (https://console.bluemix.net/docs/services/speech-to-text/language-create.html#addWords)


6. Train the model

	This step should always be done whenever more corpora files or words are added. To train, just make a POST request to the custom language model:
	```bash
	curl -X POST -u "<username>:<password>"  "https://stream.watsonplatform.net/speech-to-text/api/v1/customizations/<customization-id>/train"
	```
7. Monitor the training process:

	```bash
	curl -X GET -u  "<username>:<password>" "https://stream.watsonplatform.net/speech-to-text/api/v1/customizations/<customization-id>"
	```
	Returns:
	```json
	{
	"owner": "752f5526-2624-4e8e-aa4b-1814ffe4db0d",
	"base_model_name": "es-ES_NarrowbandModel",
	"customization_id": "e4766090-ba51-11e7-be33-99bd3ac8fa93",
	"dialect": "es-LA",
	"created": "2017-10-26T13:30:54.617Z",
	"name": "Chile Custom Language Model Example",
	"description": "Example language model for chilean speakers",
	"progress": 0,
	"language": "es-ES",
	"status": "training"
	}
	```
	The response includes status and progress fields that report the current state of the custom model; the meaning of the progress field depends on the model's status. The status field can have one of the following values:

	+ `pending` - indicates that the model was created but is waiting either for training data to be added or for the service to finish analyzing data that was added. The progress field is 0.
	+ `ready` - indicates that the model is ready to be trained. The progress field is 0.
	+ `training` - indicates that the model is currently being trained. The progress field indicates the progress of the training as a percentage complete.

	Note: The progress field does not currently reflect the progress of the training. The field changes from 0 to 100 when training is complete.
	available indicates that the model is trained and ready to use. The progress field is 100.
	failed indicates that training of the model failed. The progress field is 0.


#### References

- Creating a custom Language Model - https://console.bluemix.net/docs/services/speech-to-text/language-create.html#createModel


