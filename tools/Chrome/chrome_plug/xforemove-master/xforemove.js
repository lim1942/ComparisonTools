chrome.webRequest.onHeadersReceived.addListener(function (details) {
        return {
            responseHeaders : details.responseHeaders.filter(function (header) {
                return !(/^x-frame-options$/i.test(header.name))
            })
        }
    },
    {urls: ["<all_urls>"]},
    ["blocking", "responseHeaders"]
);
