// Erin's JS Code
Notification.requestPermission().then(perm => {
    if (perm === "granted") {
        console.log("Permission granted!");
    }else{
        console.log("Permission denied!");
    }
});

pubnub.addListener({
    message: function(message) {
        // Check if the value exceeds 1000
        if (message.message.variable > 1000) {
            // Trigger a notification
            const notification = new Notification('Warning', {
                body: 'The value has exceeded 1000!',
                icon: "logo1.png",
            });
        }
    }
});
// End of Erin's JS Code