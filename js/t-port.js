document.addEventListener("DOMContentLoaded", () => {
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
    viewAllLink.addEventListener("click", toggleAllFAQs);

    // Add individual toggle functionality for each FAQ
    faqItems.forEach((item) => {
        const question = item.querySelector(".faq-question");

        question.addEventListener("click", () => {
            item.classList.toggle("active");
        });
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const ham = document.querySelector(".ham");
    const mobileMenu = document.querySelector(".mobile-menu");

    ham.addEventListener("click", () => {
        mobileMenu.classList.toggle("open");
    });
});
