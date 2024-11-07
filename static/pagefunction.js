function toggleDashboard() {
    let dashboard = document.getElementById("dashboard");
    if (dashboard.style.left === "-250px") {
        dashboard.style.left = "0";
        document.querySelector('.content').style.marginLeft = "250px"; // Show dashboard
    } else {
        dashboard.style.left = "-250px";
        document.querySelector('.content').style.marginLeft = "0"; // Hide dashboard
    }
}

// Wait for the DOM content to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get a reference to the logout button
    var logoutButton = document.querySelector('.logoutBtn');

    // Check if the logout button exists
    if (logoutButton) {
        // Add an event listener to the logout button
        logoutButton.addEventListener('click', function() {
            // Code to logout user goes here...
            alert("Logged out successfully!");
        });
    } else {
        console.error('Logout button not found');
    }
});
