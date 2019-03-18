## Using Grammars for Speech Recognition <!-- omit in toc -->


This guide is to show you how to use grammars with IBM Voice Gateway. With the IBM Speech-To-Text service one can uses grammars to specify how to form valid strings from the language's alphabet. When you use a custom language model and a grammar for speech recognition, the service can return a valid phrase from the grammar or an empty result. Grammars are useful when you need to recognize specific words or phrases, such as **yes** or **no**, individual letters, numbers as well as alphanumerical combinations.

For more information on grammars with IBM Speech-To-Text service https://cloud.ibm.com/docs/services/speech-to-text?topic=speech-to-text-grammars#grammars

First you'll need to create a custom language model as well as a grammar to use, you can follow the steps defined in: [Adding a grammar to a custom language model](https://cloud.ibm.com/docs/services/speech-to-text?topic=speech-to-text-grammarAdd#grammarAdd)

Here are a some options of using grammars with IBM Voice Gateway:- [Using Grammars for Speech Recognition](#using-grammars-for-speech-recognition)

- [Setting a grammar from Watson Assistant](#setting-a-grammar-from-watson-assistant)
- [Advanced JSON Configuration](#advanced-json-configuration)

### Setting a grammar from Watson Assistant

Generally, you may want to use a grammar to recognize some kind of an expected phrase, for example matching an alpha numerical combination. By using the `vgwActSetSTTConfig` action from a Watson Assistant Dialog node you can modify the Speech recognition configuration to use grammar for just an input from the user or you can set it for the rest of the conversation.

For example, in your Watson Assistant Dialog node, specify the `vgwActSetSTTConfig`, as the action `vgwAction` to use, it would use the following structure:

```json

{
  "output": {
    "text": {
      "values": [
        "Hey, testing a grammar input!"
      ],
      "selection_policy": "sequential"
    },
    "vgwAction": {
      "command": "vgwActSetSTTConfig",
      "parameters": {
        "updateMethod": "mergeOnce",
        "config": {
          "grammar_name": "{your_grammar_name}",
          "language_customization_id": "{your_language_customization_id}"
        }
      }
    }
}
```

As you can see, `updateMethod` set to `mergeOnce` specifies that the grammar will be merged and used once on the user input. If it is set to `merge`, the grammar will be merged to the existing speech recognition configuration for the rest of the conversation.

For more information on the `vgwActSetSTTConfig` action, see [Dynamically configuring the Speech to Text service](https://www.ibm.com/support/knowledgecenter/SS4U29/dynamicstt.html) for more information.



### Advanced JSON Configuration

You can specify it through the [Advanced JSON Configuration](https://www.ibm.com/support/knowledgecenter/SS4U29/json_config_props.html). This configuration will be used for all recognition requests by the IBM Voice Gateway. You can modify the configuration using the `vgwActSetSTTConfig` action from a Watson Assistant Dialog node, see [Dynamically configuring the Speech to Text service](https://www.ibm.com/support/knowledgecenter/SS4U29/dynamicstt.html) for more information.

```javascript
{
  "tenants": [{
    "tenantURI": "2345556789",
    "description": "Voice Gateway Demo",
    "conversation": {
        ...
    },
    "stt": {
      "credentials": {
        "url": "https://stream.watsonplatform.net/speech-to-text/api",
        "username": "9h7f54cb-f28f-4a64-91e1-a0657e1dd3f4",
        "password": "IAB5jfxls0Zt"
      },
      "config": {
        "model": "en-US_NarrowbandModel",
        "language_customization_id": "{your_customization_id}",
        "grammar_name": "{your_grammar_name}"
        "profanity_filter": true,
        "smart_formatting": true
      }
    },
    "tts": {
        ...
    }
  }]
}
```

