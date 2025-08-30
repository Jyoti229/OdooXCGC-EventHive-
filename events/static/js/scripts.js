// Script to toggle the sidebar on mobile screens
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('active');
}

// Function to open and close the sidebar
function openSidebar() {
    document.getElementById('sidebar').style.transform = "translateX(0)";
}

function closeSidebar() {
    document.getElementById('sidebar').style.transform = "translateX(-100%)";
}

// Script to handle the hero section CTA button click
document.querySelector('.cta-button').addEventListener('click', function(event) {
    event.preventDefault();
    window.location.href = "/events/"; // Replace with the actual page you want to direct users to
});

// Optional: Modal Image Gallery for featured events (if you want to implement image modals)
function onClick(element) {
    const modal = document.getElementById("modal01");
    const img = document.getElementById("img01");
    const caption = document.getElementById("caption");
    img.src = element.src;
    caption.innerHTML = element.alt;
    modal.style.display = "block";
}

document.getElementById("modal01").addEventListener("click", function() {
    this.style.display = "none";
});
