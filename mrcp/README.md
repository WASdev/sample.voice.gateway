# Integrating IBM® Voice Gateway with MRCPv2 Speech Recognizer and Synthesizers

You can configure your IBM® Voice Gateway deployment to integrate with third-party speech to text and text to speech services by using Media Resource Control Protocol Version 2 (MRCPv2) connections. Version 1.0.0.7 and later. For more information click [here](https://www.ibm.com/support/knowledgecenter/SS4U29/MRCP_stt.html
)

+ [Connecting to an MRCPv2 recognizer](https://www-03preprod.ibm.com/support/knowledgecenter/SS4U29/MRCP_stt.html)
+ [Connecting to an MRCPv2 synthesizer](https://www-03preprod.ibm.com/support/knowledgecenter/SS4U29/MRCP_tts.html)

This directory contains the following items:

+ `grammar-samples/`: Grammars defined in XML documents that are used by the MRCPv2 Speech recognizer to interpret the user's input.
+ `unimrcpConfig/`: Contains the MRCPv2 client (`unimrcp`) configuration, this defines configuration items such as the MRCPv2 server to connect to. For a full list of configuration item for the MRCPv2 client see the [UniMRCP Client Configuration Doc](http://www.unimrcp.org/manuals/html/ClientConfigurationManual.html).
+ `docker-compose.yml`: Minimum required network configuration for the IBM Voice Gateway docker containers to integrate with MRCPv2 Recognizer and Synthesizers.
+ `sample-mrcp-conversation.json`: Sample Watson Assistant Workspace JSON file, this can be used as a starting template for how to use grammars from Watson Assistant. You can import the JSON as a workspace in your Watson Assistant dashboard.
+ `tenantConfiguration.json`: Sample JSON configuration file for MRCPv2 enabled voice agents, here you can specify parameters, such as headers fields, to be used in requests to MRCPv2 recognizer and synthesizers.

