// Select the hamburger button and sidebar
const hamburgerButton = document.querySelector('.hamburger-button');
const sidebar = document.querySelector('.sidebar-div');

// Add event listener to toggle sidebar
hamburgerButton.addEventListener('click', () => {
    if (sidebar.style.marginLeft === '0px') {
        sidebar.style.marginLeft = '-250px'; // Hide the sidebar
    } else {
        sidebar.style.marginLeft = '0px'; // Show the sidebar
    }
    
});

document.addEventListener("DOMContentLoaded", function () {
    fetch("./CST401/syllabus_structure.html")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.text();
        })
        .then(data => {
            document.querySelector(".syllabus-div").innerHTML = data;
        })
        .catch(error => console.error("Error loading syllabus:", error));
});
