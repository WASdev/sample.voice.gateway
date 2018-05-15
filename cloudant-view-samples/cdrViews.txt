{
  "_id": "_design/cdrDesignDoc",
  "views": {
    "calls_by_date": {
      "reduce": "_count",
      "map": "function(doc) {\n  var date = new Date(doc.event.stopTime);\n  var year = date.getFullYear();\n  var month = date.getMonth() + 1;\n  var day = date.getDate();\n  var hours = date.getHours();\n  var minutes = date.getMinutes();\n  var seconds = date.getSeconds();\n  var key = year + \"/\" + month + \"/\" + day + \" \" + hours + \":\" + minutes + \":\" + seconds;\n  emit(key, (doc.event.callLength) / (60 * 1000));\n}"
    },
    "call_minutes_by_date": {
      "reduce": "_sum",
      "map": "function(doc) {\n  var date = new Date(doc.event.stopTime);\n  var year = date.getFullYear();\n  var month = date.getMonth() + 1;\n  var day = date.getDate();\n  var hours = date.getHours();\n  var minutes = date.getMinutes();\n  var seconds = date.getSeconds();\n  var key = year + \"/\" + month + \"/\" + day + \" \" + hours + \":\" + minutes + \":\" + seconds;\n  emit(key, (doc.event.callLength) / (60 * 1000));\n}"
    }
  },
  "language": "javascript"
}
