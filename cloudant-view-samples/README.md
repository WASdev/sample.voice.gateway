# Cloudant View Samples
-------------------
Since the Product Insights service is being deprecated, there needs to be an alternate way to gather usage data from the Voice Gateway.     A feature was added in release 1.0.0.5d of the gateway, that enables publishing of Call Detail Records (CDRs) to a Cloudant database (find more info [here](https://www.ibm.com/support/knowledgecenter/en/SS4U29/reportingcdr.html)).    This directory contains a design document with sample views that allows the user to determine this information:
* Call minutes handled by the Voice Gateway over a specified time.     
* Number of calls handled by the Voice Gateway over a specified time.


To add these views to your CDR database, please follow these instructions:
 1.  Go to the "Design Documents" section, and click "New Doc".
 2.  The dashboard creates the outline of a document that includes an id.    Remove that id.
 3.  In the samples repo, open the "cdrViews.txt" file.    Copy the code from this file and paste it into the Cloudant document.
 4.  Click "Create document"
 
 <br/>
In the dashboard, you will see that a new design document has been created called "_design/cdrDesignDoc".    This contains the two views, "calls_by_date" and "call_minutes_by_date".
<br/>

### calls_by_date view:
If you access the "calls_by_date" view, it will return the number of calls that occurred over a given time period.   Here is an example of the URL which accesses the view.    The reduce function is set to "true", and the start and end keys are set to the dates  we are interested in:<br/>
`https://XXX-bluemix.cloudant.com/vgw-svt/_design/cdrDesignDoc/_view/calls_by_date?reduce=true&startkey=%222018/04/18%2000:00:00%22&endkey=%222018/04/18%2023:59:59%22`

This view basically creates a map in the database where the key is the date string, and the value is the call length (in minutes).    Since the "reduce" parameter is set to "true", it runs a "_count" on the number of records listed between the "startkey" and "endkey".    This results in the number of calls that occurred between the start and end dates (inclusive).

### call_minutes_by_date view:
Here is an example of the URL which accesses the "call_minutes_by_date" view:<br/>
`https://XXX-bluemix.cloudant.com/vgw-svt/_design/cdrDesignDoc/_view/call_minutes_by_date?reduce=true&startkey=%222018/04/18%2000:00:00%22&endkey=%222018/04/18%2023:59:59%22`

The "call_minutes_by_date" view uses the "startkey" and "endkey" to determine which records to examine.    Since the "reduce" parameter is set to "true", it runs a "_sum" on the map values listed between the "startkey" and "endkey".    This results in the number of call minutes that occurred between the start and end dates (inclusive).
