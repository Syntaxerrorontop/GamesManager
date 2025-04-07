chrome.webRequest.onHeadersReceived.addListener(
    function(details) {
        // Check if the status code is a redirect (e.g., 302)
        if (details.statusCode === 302) {
            // If the response code is 302, it's a redirect
            console.log('Redirect detected! Status Code:', details.statusCode);
    
            // Look for the Location header to get the redirect URL
            let locationHeader = details.responseHeaders.find(header => header.name.toLowerCase() === 'location');
            
            // If the Location header is present
            if (locationHeader) {
                // If the redirect URL is not the one we are monitoring, log it
                if(locationHeader.value !== "https://megadb.net/download"){
                    console.log('DDL Detected: sending to DownloadManager', locationHeader.value);

                    // Send only the Location header value to your Python app
                    fetch("http://localhost:5000/headers", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            location: locationHeader.value // Send only the locationHeader.value
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log("Successfull", data);
                        return { cancel: true };
                    })
                    .catch(error => {
                        console.error("Error", error);
                    });
                }
            }
        }
    },
    {
        // Match all requests to the domain megadb.net (or specific URLs if you want)
        urls: ["https://megadb.net/*"]
    },
    // Capture response headers to check for the Location header
    ["responseHeaders"]
);
