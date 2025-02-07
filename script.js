document.addEventListener("DOMContentLoaded", function() {
    fetch("https://api.ipstack.com/check?access_key=YOUR_IPSTACK_KEY")
    .then(response => response.json())
    .then(data => {
        document.getElementById("address").value = `${data.city}, ${data.region_name}, ${data.country_name}`;
    })
    .catch(error => console.error("Error fetching geolocation:", error));
});
