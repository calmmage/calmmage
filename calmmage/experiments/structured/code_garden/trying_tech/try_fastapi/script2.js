function sendAddDataRequest() {
    document.getElementById("add-status").innerHTML = "Add status: Processing...";
    document.getElementById("add-button").disabled = true;

    const key = document.getElementById("add-key").value;
    const value = document.getElementById("add-value").value;

    // const response = await fetch(`http://localhost:8000/${key}`, {
    //     method: "PUT",
    //     headers: {"Content-Type": "application/json"},
    //     body: JSON.stringify({value: value})
    // });
    const response = fetch(`http://localhost:8000/data2/${key}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({value})
    });
    // const requestData = {
    //   "Id": 12345,
    //   "Customer": "John Smith",
    //   "Quantity": 1,
    //   "Price": 10.00
    // };
    //
    // const options = {
    //   method: 'PUT',
    //   headers: {
    //     'Content-Type': 'application/json',
    //     'Content-Length': JSON.stringify(requestData).length
    //   },
    //   body: JSON.stringify(requestData)
    // };
    //
    // const url = 'https://reqbin.com/echo/put/json';
    //
    // fetch(url, options)
    //   .then(response => response.json())
    //   .then(data => console.log(data))
    //   .catch(error => console.error(error));


    document.getElementById("add-status").innerHTML = "Add status: Success!";
    document.getElementById("add-response").innerHTML = response.text();

    document.getElementById("add-key").value = "";
    document.getElementById("add-value").value = "";
    document.getElementById("add-button").disabled = false;
}

function sendGetDataRequest() {
    document.getElementById("get-status").innerHTML = "Get status: Processing...";
    document.getElementById("get-button").disabled = true;

    const key = document.getElementById("get-key").value;

    fetch(`http://localhost:8000/data2/${key}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            document.getElementById("get-status").innerHTML = "Get status: Success!";
            document.getElementById("get-response").innerHTML = response.status().toString();

            document.getElementById("get-key").value = "";
            document.getElementById("get-button").disabled = false;
        })
        .then(data => {
            // Do something with the response data
            console.log(data);
        })
        .catch(error => {
            // Handle the error
            console.error(error);
        });
    // const response = await fetch(`http://localhost:8000/${key}`);
    // const future = fetch();
    // const response = future.then(response => response.json());
    // const result = await response;
    // document.getElementById("get-response").innerHTML = response.json();
    // document.getElementById("get-response").innerHTML = "blah blah!";

}