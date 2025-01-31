document.addEventListener('DOMContentLoaded', function () {

    console.log("Honeypot script loaded");

    const honeypotButton = document.getElementById('honeypotbutton');
    const honeypotField = document.getElementById('honeypotfield'); // May not exist on all pages
    const honeypotLink = document.getElementById('honeypotlink');
    
    // Check if the honeypot button exists
    if (honeypotButton) {
        honeypotButton.addEventListener('click', function () {
            // Toggle honeypot link visibility
            if (honeypotLink) {
                if (honeypotLink.style.display === 'block') {
                    honeypotLink.style.display = 'none';
                    honeypotButton.textContent = 'Show Honeypot Link'; // Change button text
                } else {
                    honeypotLink.style.display = 'block';
                    honeypotButton.textContent = 'Hide Honeypot Link'; // Change button text
                }
            }

            // Toggle honeypot field visibility only if it exists
            if (honeypotField) {
                if (honeypotField.style.display === 'block') {
                    honeypotField.style.display = 'none';
                } else {
                    honeypotField.style.display = 'block';
                }
            }
        });
    } else {
        console.error("Honeypot button not found in the DOM.");
    }
});
