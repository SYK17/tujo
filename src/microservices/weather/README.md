# weatherMicroservice
## Requirements
Node.js is required to run the javascript files. Node.js is needed. It can be found and installed here https://nodejs.org/en  
There are no dependancies (that dont come pre-packaged in Node.js). (Nodemon was a dependancy for development, but it is not needed to run the server). Therefore NPM isnt required.

Once you have Node.js, all you will need to o to run the microservice is: Download weather.js , and (after navigating to the downloaded file) run `node weather.js` in a terminal window.
## Communication Contract
### Request Data
Ensure the microservice is running (with npm run weatherProccess)  
Make a POST request to http://localhost:3724/weatherMicro. Reccomended to make the headers: `{'Content-Type': 'application/json'}`. Ensure you are sending a json.  
The body of the POST request's JSON should be `{zip: "(zipcode)", operation:"current", addInfo: "0"}`, with `(zipcode)` being replaced with the zipcode you wish to use.  

### Recieve Data
To recieve the data, do the above in an asyncronous function, and assign the response of the request to a variable (or use it directly. You just need to agnowledge that the data is a direct response to the post request. A seperate response will not be made).

### Example (of both)
send.js (in the root folder) provides an example of how to do both of these (at the same time). For the sake of assingment completion, here it is again:
```
const fetch = require('node-fetch');

async function sendRequest() {
  const body = {zip: "14534", operation:"current", addInfo: "0"};

  const options = {
    method: 'POST',
    body: JSON.stringify(body),
    headers: {'Content-Type': 'application/json'}
  };

  const response = await fetch('http://localhost:3724/weatherMicro', options);
  const data = await response.json();
  console.log(data);
}

sendRequest();
```

### UML
A diagram can be rendered from https://sequencediagram.org/ by simply pasting the data in umlDiagram.txt
