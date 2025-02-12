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

document.addEventListener("DOMContentLoaded", () => {
    const syllabusDiv = document.querySelector(".syllabus-div");

    // Function to load new content into the div
    function loadContent(url) {
        fetch(url)
            .then(response => response.text())
            .then(data => {
                syllabusDiv.innerHTML = data;
            })
            .catch(error => console.error("Error loading content:", error));
    }

    // Event delegation for handling clicks inside the content div
    syllabusDiv.addEventListener("click", (event) => {
        if (event.target.tagName === "A") {
            event.preventDefault(); // Stop the default link behavior
            const url = event.target.getAttribute("href"); // Get href attribute
            loadContent(url); // Fetch new content
        }
    });

});
