//Sends an example request to test/demonstrate functionality of the microservice.
//This file should not be needed for the program that uses the microservice. That being said, feel free to reference it to look at what a request should look like.
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