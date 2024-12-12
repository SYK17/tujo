//A simple server created directly with node

import { default as http } from "http";
const port = 8000;

const server = http.createServer((req, res) => {
  console.log("Request for " + req.url);
  if (req.url == "/receive")
  try {
    let body = '';
    if (req.method === 'POST') {
      req.on('data', chunk => {
          body += chunk.toString(); // convert Buffer to string
      });
      req.on('end', () => {

        //This is where the rest of the code goes
        if (body == "") {
          body = "blank";
        }

        //Try to read and return the input
        console.log(body);
        res.statusCode = 200;
        res.setHeader("Content-Type", "application/json");
        res.end(JSON.stringify({response: 'solid copy'}));


        //any code manipulating or parsing data or doing whatever needs to remain within this bracket.
        //the bodys data dissapears afterwards


      });
    }
  } catch (err) {
    res.statusCode = 500;
    console.log(err +" err");
    res.setHeader("Content-Type", "application/json");
    res.end(JSON.stringify({response: "<p>Server fail. Please check the logs</p>"}));
  }
});

server.listen(port, () => {
  console.log(`Server running at port ${port}`);
});