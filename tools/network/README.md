# Voice Gateway Tools - Network

This folder contains tools you can use to debug voice gateway networking related issues. The focus here is on tools that can help you identify hybrid-cloud networking issues that could be causing voice gateway issues like socket timeouts and call latencies.

## Watson Assistant Curl Script: wa-curl.sh

This bash script will issue periodic request to Watson Assistant (default period is every 2 seconds) and will print out cases where the response time exceeds a predefined threshold (default threshold is 2 seconds). This WA request does not include input text so a new conversation-id will be generated on every request. The curl command generates all of the following:

- **HTTP Response Headers** - needed to access transaction IDs
- **JSON Response from Watson Assistant** - which includes the conversation ID 
- **Time Elements** - which provide details about where time was spent during the transaction

Note that this script first dumps all the results to a file (results.txt) and then uses awk to parse the last line of the file to get the total transaction time. 

Here is an example of the response that is returned from this script:

```
time: 02/28/2019 15:47:47
HTTP/2 200 
x-backside-transport: OK OK
content-type: application/json; charset=utf-8
access-control-allow-origin: *
access-control-allow-methods: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
access-control-allow-headers: Content-Type, Content-Length, Authorization, X-Watson-Authorization-Token, X-WDC-PL-OPT-OUT, X-Watson-UserInfo, X-Watson-Learning-Opt-Out, X-Watson-Metadata
access-control-max-age: 3600
content-security-policy: default-src 'none'
x-dns-prefetch-control: off
x-frame-options: SAMEORIGIN
strict-transport-security: max-age=31536000;
x-download-options: noopen
x-content-type-options: nosniff
x-xss-protection: 1; mode=block
x-global-transaction-id: 7ecac92c5c7848f316aa17ed
x-dp-watson-tran-id: gateway01-380245997
x-dp-transit-id: gateway01-380245997
content-length: 411
date: Thu, 28 Feb 2019 20:47:47 GMT

{"intents":[],"entities":[],"input":{"text":""},"output":{"text":["Hi, my name is Watson. What can I do for you today?"],"nodes_visited":["Introduction"],"log_messages":[]},"context":{"conversation_id":"e13622f3-0816-4656-ad0f-5c187fefc5a4","system":{"initialized":true,"dialog_stack":[{"dialog_node":"Introduction"}],"dialog_turn_counter":1,"dialog_request_counter":1,"_node_output_map":{"Introduction":[0]}}}} 
lookup:        0.061419
connect:       0.121267
appconnect:    3.288581
pretransfer:   3.288919
redirect:      0.000000
starttransfer: 3.288951
total:         3.423352
```
First is the HTTP response headers. Second is the actual JSON response from WA and then all the time elements. Here are the definitations for each of the time elements:

- **time**: The time that the curl command was issued.
- **lookup**: The time, in seconds, it took from the start until the name resolving was completed.
- **connect**: The time, in seconds, it took from the start until the TCP connect to the remote host (or proxy) was completed.
- **appconnect**: The time, in seconds, it took from the start until the SSL/SSH/etc connect/handshake to the remote host was completed. (Added in 7.19.0)
- **pretransfer**: The time, in seconds, it took from the start until the file transfer was just about to begin. This includes all pre-transfer commands and negotiations that are specific to the particular protocol(s) involved.
- **redirect**: The time, in seconds, it took for all redirection steps include name lookup, connect, pretransfer and transfer before the final transaction was started. time_redirect shows the complete execution time for multiple redirections. (Added in 7.12.3)
- **starttransfer**: The time, in seconds, it took from the start until the first byte was just about to be transferred. This includes time_pretransfer and also the time the server needed to calculate the result.
- **total**: The total time, in seconds, that the full operation lasted. The time will be displayed with millisecond resolution.

To run this script you will need to do the following:

1. If you are running on a MacOS, you will need to install the GNU implementation of awk. Its needed for the accessing systime. Its really easy to do this using **homebrew** like this: ```brew install gawk``` (note that this step is not needed on other Linux systems)
1. You will need to modify the wa-curl.sh file with your Watson Assistant details including credentials and workspace ID. Look for the following tags to modify ```username```, ```password``` and ```workspace-id```
1. If you want to change either the periodicity of the script or the latency threshold it should be easy to see in the script how to do that.
1. Run the script like this ```./wa-curl.sh > output.txt ```

**Note that this script currently supports the v1 Watson Assistant API. You can pass an API-KEY to it by setting the username to ```apikey``` and password to the actual api key value.**