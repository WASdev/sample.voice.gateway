# How to use a different voice than the default one in the welcome node of your Conversation.

There is one specific voice that is considered default for a given TTS language. For instance, `en-US_MichaelVoice` is the default voice for American English. 
If you would like to start your conversation using `en-US_LisaVoice` instead, use this snippet in the welcome node of WCS:
```json
{
    "output": {
        "vgwActionSequence": [{
            "command": "vgwActSetTTSConfig",
            "parameters": {
                "config": {
                    "voice": "en-US_LisaVoice"
                }
            }
        }, {

            "command": "vgwActPlayText",
            "parameters": {
                "text": [
                    "Hello World!"
                ]
            }
        }]
    }
}

```
