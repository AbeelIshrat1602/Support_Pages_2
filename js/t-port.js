document.addEventListener("DOMContentLoaded", () => {
    // FAQ toggle functionality
    const faqItems = document.querySelectorAll(".faq-item");
    const viewAllLink = document.getElementById("view-all-link");
    let allExpanded = false; // Tracks whether all FAQs are expanded or collapsed

    // Function to toggle all FAQs
    const toggleAllFAQs = () => {
        faqItems.forEach((item) => {
            if (allExpanded) {
                item.classList.remove("active"); // Collapse all
            } else {
                item.classList.add("active"); // Expand all
            }
        });

        // Update the text of the "View All" link
        viewAllLink.textContent = allExpanded ? "View All" : "Collapse All";

        // Toggle the allExpanded state
        allExpanded = !allExpanded;
    };

    // Add event listener to "View All" link
    if (viewAllLink) {
        viewAllLink.addEventListener("click", toggleAllFAQs);
    }

    // Add individual toggle functionality for each FAQ
    faqItems.forEach((item) => {
        const question = item.querySelector(".faq-question");

        question.addEventListener("click", () => {
            item.classList.toggle("active");
        });
    });

    // Hamburger menu toggle functionality
    const ham = document.querySelector(".ham");
    const mobileMenu = document.querySelector(".mobile-menu");

    if (ham && mobileMenu) {
        ham.addEventListener("click", () => {
            mobileMenu.classList.toggle("open");
        });
    }

    // Feedback Widget Integration
    const injectFeedbackWidget = () => {
        // Dynamically adjust the path to "feedback-widget.html"
        let basePath = window.location.pathname.includes('/support-pages/')
            ? '/feedback-widget.html' // If in a nested page
            : './feedback-widget.html'; // If at the root directory

        fetch(basePath)
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Failed to load feedback widget');
                }
                return response.text();
            })
            .then((html) => {
                document.body.insertAdjacentHTML('beforeend', html); // Inject Feedback Widget
            })
            .catch((error) => console.error('Error loading the Feedback Widget:', error));
    };

    injectFeedbackWidget(); // Inject the widget into all pages
});