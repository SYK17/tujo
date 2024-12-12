//Sends an example request to test/demonstrate functionality of the microservice.
//This file should not be needed for the program that uses the microservice. It will also likely be irrelevant to that project.
const fetch = require('node-fetch');

async function sendHistoryRequest() {
  const body = {zip: "14534", operation:"history", addInfo: "2024-01-01"};  //date

  const options = {
    method: 'POST',
    body: JSON.stringify(body),
    headers: {'Content-Type': 'application/json'}
  };

  const response = await fetch('http://localhost:3724/weatherMicro', options);
  const data = await response.json();
  console.log(data);
}

sendHistoryRequest();

async function sendForecastRequest() {
  const body = {zip: "14534", operation:"forecast", addInfo: "2"}; //2 days in the future

  const options = {
    method: 'POST',
    body: JSON.stringify(body),
    headers: {'Content-Type': 'application/json'}
  };

  const response = await fetch('http://localhost:3724/weatherMicro', options);
  const data = await response.json();
  console.log(data);
}

sendForecastRequest();