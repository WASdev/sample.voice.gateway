Sometimes Watson TTS will not be able to synthesize foreign words correctly. 
There are at least 2 ways to approach that:

1.	Easier route: One can write the word as it sounds in the target TTS Voice. For instance, if the English word “Voice” would be used in a German voice de-DE_Birgit, it could be written as “Voiss” and provide a closer result to the desired pronunciation. Other  examples are “Watson” which could be written “Uats-SSon”; or “Center” could be written “SSenter” (for the same German voice de-DE_Birgit.

2.	A more elaborate route:  Sometimes the easier route will not work well. In those cases, one needs to use TTS customization. For example, “Knowledge” could be written ' <phoneme alphabet="ibm" ph="nolEdZ"> Knowledge </phoneme> '. More details for TTS customization here:  https://console.bluemix.net/docs/services/text-to-speech/SPRs.html#supportedLanguages

Here’s a Watson demo tool that allows you test TTS renditions on any supported language:  https://text-to-speech-demo.ng.bluemix.net/
