const fetch = require('node-fetch');

async function sendRequest() {
  const body = {"message": "This is a message from CS361"};

  const options = {
    method: 'POST',
    body: JSON.stringify(body),
    headers: {'Content-Type': 'application/json'}
  };

  const response = await fetch('http://localhost:8000/receive', options);
  const data = await response.json();
  console.log(data);
}

sendRequest();