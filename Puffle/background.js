chrome.runtime.onMessage.addListener(function(request, sender) {
    chrome.tabs.update(sender.tab.id, {url: request.redirect});
});

chrome.tabs.onUpdated.addListener( function(tabId, changeInfo, tab) {
    chrome.tabs.getSelected(null, function(tab){
        url = tab.url;
        if (url.indexOf('facebook') !== -1 || url.indexOf('twitter') !== -1 || url.indexOf('youtube') !== -1) {
          chrome.tabs.update({
            url:"http://127.0.0.1:5000/badpage"
          });
        }
    });
});
