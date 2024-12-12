// NOTE: This microservice was created by a partner.
// All other microservices were created by me.

const fetch = require('node-fetch');
const http = require('http');

//A simple server created directly with node

const port = 3724;

const server = http.createServer((req, res) => {
    console.log("Request for " + req.url);
    if (req.url == "/weatherMicro")
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
                    //console.log(body);
                    let data = JSON.parse(body);
                    console.log(data);
                    //getData(data.zip, data.operation, data.addInfo);
                    let resp = (async() =>{
                        try {
                            //Make web request for data
                            const key = 'eca6cf01e878401ba7c205537240411';
                            //let zipcode = 14534;
                            let url = "http://api.weatherapi.com/v1/"+ data.operation + ".json?key="+ key + '&q=' + data.zip;
                            if (data.operation != "current"){
                                if (data.operation == "forecast")
                                    url = url + '&days=' + data.addInfo;
                                    else if (data.operation == "history")
                                        url = url + '&dt=' + data.addInfo;
                                        else throw ("Op cannot be " + data.operation);
                            }
                            //console.log(url);
                            let response = await fetch(
                                //"http://api.weatherapi.com/v1/"+ operation + ".json?key="+key + '&q=' + zipcode +"&aqi=no"
                                url + "&aqi=no");
                            //Make sure response code was OK
                            if (response.status != 200)
                                throw response.status + " " + response.statusText;

                            //Convert response data to json
                            let returnedData = await response.json();
                            //console.log(returnedData);
                            //Now use json data

                            //useData ({temp:returnedData.current.temp_f, cond:returnedData.current.condition.text, icon:returnedData.current.condition.icon});
                            if (data.operation == "current")
                                resp = {temp:returnedData.current.temp_f, cond:returnedData.current.condition.text, icon:returnedData.current.condition.icon};
                                else if (data.operation == "forecast") 
                                    resp = {temp:returnedData.forecast.forecastday[data.addInfo-1].day.avgtemp_f, cond:returnedData.forecast.forecastday[data.addInfo-1].day.condition.text, icon:returnedData.forecast.forecastday[data.addInfo-1].day.condition.icon}
                                    else //history. if it wernet it would have errored out
                                    resp = {temp:returnedData.forecast.forecastday[0].day.avgtemp_f, cond:returnedData.forecast.forecastday[0].day.condition.text, icon:returnedData.forecast.forecastday[0].day.condition.icon}

                            res.statusCode = 200;
                            res.setHeader("Content-Type", "application/json");
                            //res.end(JSON.stringify({response: 'solid copy'}));
                            res.end(JSON.stringify(resp));

                            //console.log(returnedData.current.temp_f + ' ' + returnedData.current.condition.text + ' ' + returnedData.current.condition.icon + ";");

                        } catch (error) {
                            res.statusCode = 500;
                            console.log(error +" err");
                            res.setHeader("Content-Type", "application/json");
                            res.end(JSON.stringify({temp:"?f", cond:error, icon:"about:blank"}));
                        }})();

                    //res.statusCode = 200;
                    //res.setHeader("Content-Type", "application/json");
                    //res.end(JSON.stringify({response: 'solid copy'}));
                    //res.end(JSON.stringify(resp));


                    //any code manipulating or parsing data or doing whatever needs to remain within this bracket.
                    //the bodys data dissapears afterwards


                });
            }
        } catch (err) {
        res.statusCode = 500;
        console.log(err +" err");
        res.setHeader("Content-Type", "application/json");
        res.end(JSON.stringify({temp:"?f", cond:"Server fail. Please check the logs", icon:"about:blank"}));
    }
});

server.listen(port, () => {
    console.log(`Server running at port ${port}`);
} );
