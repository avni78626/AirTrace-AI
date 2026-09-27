// Create map

const map = L.map("map").setView(
    [32.386, 75.517],
    10
);


// Add OpenStreetMap tiles

L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        attribution:
            "&copy; OpenStreetMap contributors"
    }
).addTo(map);


// Kathua marker

const kathua = L.marker(
    [32.386, 75.517]
).addTo(map);


kathua.bindPopup(
    `
    <b>Kathua</b>
    <br>
    Risk Level: HIGH
    <br>
    Risk Score: 72
    `
);


// High risk zone

L.circle(
    [32.386, 75.517],
    {
        radius: 5000,

        color: "red",

        fillColor: "red",

        fillOpacity: 0.2
    }
).addTo(map);


// Medium risk zone

L.circle(
    [32.45, 75.60],
    {
        radius: 3500,

        color: "orange",

        fillColor: "orange",

        fillOpacity: 0.2
    }
).addTo(map);


// Low risk zone

L.circle(
    [32.32, 75.45],
    {
        radius: 3000,

        color: "green",

        fillColor: "green",

        fillOpacity: 0.2
    }
).addTo(map);