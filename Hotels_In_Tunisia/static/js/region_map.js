let map;
let markers = [];

function initMap() {
    if (!document.getElementById('map')) return;

    const region = window.location.pathname.split('/').pop();
    const regionBounds = {
        'tunis': {
            center: [36.8065, 10.1815],
            bounds: [[36.7065, 10.0815], [36.9065, 10.2815]]
        },
        'sousse': {
            center: [35.8245, 10.6346],
            bounds: [[35.7245, 10.5346], [35.9245, 10.7346]]
        },
        'mahdia': {
            center: [35.5024, 11.0458],
            bounds: [[35.4024, 10.9458], [35.6024, 11.1458]]
        },
        'sfax': {
            center: [34.7398, 10.7600],
            bounds: [[34.6398, 10.6600], [34.8398, 10.8600]]
        },
        'djerba': {
            center: [33.8075, 10.8451],
            bounds: [[33.7075, 10.7451], [33.9075, 10.9451]]
        }
    };

    const regionData = regionBounds[region] || { center: [34.0, 9.0], bounds: null };
    map = L.map('map', {
        center: regionData.center,
        zoom: 13,
        minZoom: 12,
        maxZoom: 18
    });

    if (regionData.bounds) {
        map.setMaxBounds(regionData.bounds);
    }

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Add markers for all hotels in the region
    const hotels = document.querySelectorAll('.hotel-card');
    hotels.forEach(hotelElement => {
        const hotelId = hotelElement.dataset.hotelId;
        const lat = parseFloat(hotelElement.dataset.lat);
        const lng = parseFloat(hotelElement.dataset.lng);
        const name = hotelElement.dataset.name;

        if (!isNaN(lat) && !isNaN(lng)) {
            const marker = L.marker([lat, lng])
                .bindPopup(`
                    <strong>${name}</strong><br>
                    <button class="btn btn-sm btn-primary" onclick="showHotelDetails(${hotelId})">
                        View Details
                    </button>
                `);
            markers.push(marker);
            marker.addTo(map);
        }
    });

    // Fit bounds to markers if there are any
    if (markers.length > 0) {
        const group = new L.featureGroup(markers);
        map.fitBounds(group.getBounds().pad(0.1));
    }
}

function showHotelDetails(hotelId) {
    fetch(`/api/hotels/${hotelId}`)
        .then(response => response.json())
        .then(hotel => {
            const detailsHtml = `
                <h4>${hotel.name}</h4>
                <p>${hotel.description}</p>
                <p><strong>Price Range:</strong> ${hotel.price_range}</p>
                ${hotel.amenities ? `<p><strong>Amenities:</strong> ${Object.keys(hotel.amenities).join(', ')}</p>` : ''}
            `;
            document.getElementById('hotelDetails').innerHTML = detailsHtml;
            const modal = new bootstrap.Modal(document.getElementById('detailsModal'));
            modal.show();
        })
        .catch(error => console.error('Error:', error));
}

function showNearbyPlaces(hotelId) {
    fetch(`/api/hotels/${hotelId}/nearby`)
        .then(response => response.json())
        .then(data => {
            const { activities, restaurants } = data;
            showNearbyList(activities, restaurants);
        })
        .catch(error => console.error('Error:', error));
}

function showNearbyList(activities, restaurants) {
    const modal = new bootstrap.Modal(document.getElementById('detailsModal'));
    let modalBodyContent = '';

    if (activities && activities.length > 0) {
        modalBodyContent += `
            <h4>Nearby Activities</h4>
            <div class="list-group mb-3">
                ${activities.map(activity => `
                    <a href="/activity/medina-tour" class="list-group-item list-group-item-action">
                        <h6 class="mb-1">${activity.name}</h6>
                        <p class="mb-1">${activity.description}</p>
                        <small>${activity.activity_type}</small>
                    </a>
                `).join('')}
            </div>`;
    }

    if (restaurants && restaurants.length > 0) {
        modalBodyContent += `
            <h4>Nearby Restaurants</h4>
            <div class="list-group">
                ${restaurants.map(restaurant => `
                    <a href="/restaurant/le-mediterranee" class="list-group-item list-group-item-action">
                        <h6 class="mb-1">${restaurant.name}</h6>
                        <small>Cuisine: ${restaurant.cuisine_type}</small>
                        <br><small>Price Range: ${restaurant.price_range}</small>
                    </a>
                `).join('')}
            </div>`;
    }

    document.getElementById('modalBody').innerHTML = modalBodyContent;
    modal.show();
}

document.addEventListener('DOMContentLoaded', initMap);