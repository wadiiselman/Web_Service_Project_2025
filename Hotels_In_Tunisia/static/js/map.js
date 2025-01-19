let map;
let markers = [];

function initMap() {
    // Center of Tunisia
    const tunisia = [34.0, 9.0];

    map = L.map('map').setView(tunisia, 7);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Add regions including Mahdia
    const regions = {
        'Tunis': [36.8065, 10.1815],
        'Sousse': [35.8245, 10.6346],
        'Mahdia': [35.5024, 11.0458],
        'Sfax': [34.7398, 10.7600],
        'Djerba': [33.8075, 10.8451]
    };

    for (let [name, coords] of Object.entries(regions)) {
        L.marker(coords)
         .bindPopup(`<strong>${name}</strong>`)
         .on('click', () => {
             console.log(`Clicked on region: ${name}`);
             loadRegionHotels(name);
         })
         .addTo(map);
    }
}

function loadRegionHotels(region) {
    // Instead of fetching hotels, redirect to the region's hotels page
    window.location.href = `/hotels/${region.toLowerCase()}`;
}

function addMarkers(locations, type) {
    // Clear existing markers
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];

    // Add new markers
    locations.forEach(location => {
        const marker = L.marker([location.latitude, location.longitude])
            .bindPopup(`
                <strong>${location.name}</strong><br>
                ${location.description}<br>
                <button class="btn btn-sm btn-primary" onclick="showNearbyPlaces(${location.id})">Show Nearby Places</button>
            `);
        markers.push(marker);
        marker.addTo(map);
    });

    // Fit map bounds to show all markers
    if (markers.length > 0) {
        const group = new L.featureGroup(markers);
        map.fitBounds(group.getBounds().pad(0.1));
    }
}

function showHotelsList(hotels) {
    const resultsDiv = document.getElementById('hotelResults');
    if (!resultsDiv) {
        console.warn('hotelResults div not found');
        return;
    }

    resultsDiv.innerHTML = `
        <h3>Hotels in Region</h3>
        <div class="list-group">
            ${hotels.map(hotel => `
                <a href="#" class="list-group-item list-group-item-action" onclick="showNearbyPlaces(${hotel.id})">
                    <h5 class="mb-1">${hotel.name}</h5>
                    <p class="mb-1">${hotel.description}</p>
                    <small>Price Range: ${hotel.price_range}</small>
                    ${hotel.distance ? `<small class="float-end">${hotel.distance.toFixed(1)} km away</small>` : ''}
                </a>
            `).join('')}
        </div>
    `;
}

function showNearbyActivities(hotelId) {
    console.log(`Showing nearby activities for hotel: ${hotelId}`);
    fetch(`/api/hotels/${hotelId}/nearby/activities`)
        .then(response => response.json())
        .then(data => {
            console.log('Received nearby activities:', data);
            const activities = [
                {
                    id: 1,
                    name: "Guided Medina Tour",
                    description: "Explore the historic Medina of Sousse with expert guides",
                    image: "/static/images/medina_tour1.jpg",
                    duration: "3 hours",
                    price: 45,
                    rating: 4.8,
                    details: {
                        schedule: "Daily tours at 9:00 AM and 2:00 PM",
                        groupSize: "Maximum 12 people",
                        included: [
                            "Professional local guide",
                            "Historical monuments visit",
                            "Traditional market experience",
                            "Cultural insights"
                        ]
                    }
                },
                {
                    id: 2,
                    name: "Beach Water Sports",
                    description: "Exciting water activities package at Sousse Beach",
                    image: "/static/images/watersports1.jpg",
                    duration: "2 hours",
                    price: 60,
                    rating: 4.5,
                    details: {
                        schedule: "Daily 10:00 AM - 5:00 PM",
                        equipment: "All equipment provided",
                        activities: [
                            "Jet skiing",
                            "Parasailing",
                            "Banana boat rides"
                        ]
                    }
                }
            ];

            let activitiesHtml = `
                <div class="row">
                    ${activities.map(activity => `
                        <div class="col-md-6 mb-4">
                            <div class="card activity-card h-100" onclick="showActivityDetails(${JSON.stringify(activity).replace(/"/g, '&quot;')})">
                                <img src="${activity.image}" class="card-img-top activity-image" alt="${activity.name}">
                                <div class="card-body">
                                    <h5 class="card-title">${activity.name}</h5>
                                    <p class="card-text">${activity.description}</p>
                                    <div class="activity-info">
                                        <span><i class="fas fa-clock"></i> ${activity.duration}</span>
                                        <span><i class="fas fa-euro-sign"></i> ${activity.price}</span>
                                        <span><i class="fas fa-star text-warning"></i> ${activity.rating}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
            document.getElementById('nearbyPlaces').innerHTML = activitiesHtml;
        })
        .catch(error => console.error('Error:', error));
}

function showActivityDetails(activity) {
    const detailsHtml = `
        <div class="card mb-4">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0">${activity.name}</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <img src="${activity.image}" class="img-fluid rounded" alt="${activity.name}">
                    </div>
                    <div class="col-md-6">
                        <div class="activity-details">
                            <h6 class="fw-bold">Details</h6>
                            <p>${activity.description}</p>
                            <div class="info-grid">
                                <div class="detail-item">
                                    <i class="fas fa-clock"></i> Duration: ${activity.duration}
                                </div>
                                <div class="detail-item">
                                    <i class="fas fa-euro-sign"></i> Price: €${activity.price} per person
                                </div>
                                <div class="detail-item">
                                    <i class="fas fa-calendar"></i> ${activity.details.schedule}
                                </div>
                                ${activity.details.groupSize ? 
                                    `<div class="detail-item">
                                        <i class="fas fa-users"></i> ${activity.details.groupSize}
                                    </div>` : ''}
                            </div>
                            ${activity.details.included ? `
                                <div class="mt-3">
                                    <h6 class="fw-bold">Included</h6>
                                    <ul class="list-unstyled">
                                        ${activity.details.included.map(item => `<li>✓ ${item}</li>`).join('')}
                                    </ul>
                                </div>
                            ` : ''}
                            ${activity.details.activities ? `
                                <div class="mt-3">
                                    <h6 class="fw-bold">Activities</h6>
                                    <ul class="list-unstyled">
                                        ${activity.details.activities.map(item => `<li>✓ ${item}</li>`).join('')}
                                    </ul>
                                </div>
                            ` : ''}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    document.getElementById('nearbyPlaces').innerHTML = detailsHtml;
}

function showNearbyRestaurants(hotelId) {
    console.log(`Showing nearby restaurants for hotel: ${hotelId}`);
    fetch(`/api/hotels/${hotelId}/nearby/restaurants`)
        .then(response => response.json())
        .then(data => {
            console.log('Received nearby restaurants:', data);
            const restaurants = [
                {
                    id: 1,
                    name: "Le Méditerranée",
                    description: "Upscale Mediterranean restaurant with sea view",
                    image: "/static/images/restaurant1.jpg",
                    menuImage: "/static/images/menu1.jpg",
                    cuisine: "Mediterranean",
                    priceRange: "Upscale",
                    rating: 4.7,
                    detailUrl: "/restaurant/le-mediterranee",
                    hours: "12:00 - 23:00",
                    menu: {
                        starters: [
                            { name: "Mediterranean Mezze Platter", price: 25 },
                            { name: "Fresh Seafood Soup", price: 18 }
                        ],
                        mains: [
                            { name: "Grilled Sea Bass", price: 45 },
                            { name: "Lamb Couscous", price: 38 }
                        ],
                        desserts: [
                            { name: "Baklava Selection", price: 15 }
                        ]
                    }
                },
                {
                    id: 2,
                    name: "Café Tunisien",
                    description: "Traditional Tunisian cuisine in a charming setting",
                    image: "/static/images/restaurant2.jpg",
                    menuImage: "/static/images/menu2.jpg",
                    cuisine: "Tunisian",
                    priceRange: "Moderate",
                    rating: 4.5,
                    hours: "11:00 - 22:00",
                    menu: {
                        starters: [
                            { name: "Traditional Tunisian Salad", price: 12 },
                            { name: "Harissa & Bread", price: 8 }
                        ],
                        mains: [
                            { name: "Couscous Royal", price: 28 },
                            { name: "Grilled Fish of the Day", price: 32 }
                        ],
                        desserts: [
                            { name: "Assorted Tunisian Pastries", price: 14 }
                        ]
                    }
                }
            ];

            let restaurantsHtml = `
                <div class="row">
                    ${restaurants.map(restaurant => `
                        <div class="col-md-6 mb-4">
                            <div class="card restaurant-card h-100" onclick="showRestaurantDetails(${JSON.stringify(restaurant).replace(/"/g, '&quot;')})">
                                <img src="${restaurant.image}" class="card-img-top restaurant-image" alt="${restaurant.name}">
                                <div class="card-body">
                                    <h5 class="card-title">${restaurant.name}</h5>
                                    <p class="card-text">${restaurant.description}</p>
                                    <div class="restaurant-info">
                                        <span><i class="fas fa-utensils"></i> ${restaurant.cuisine}</span>
                                        <span><i class="fas fa-tag"></i> ${restaurant.priceRange}</span>
                                        <span><i class="fas fa-star text-warning"></i> ${restaurant.rating}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
            document.getElementById('nearbyPlaces').innerHTML = restaurantsHtml;
        })
        .catch(error => console.error('Error:', error));
}

function showRestaurantDetails(restaurant) {
    const detailsHtml = `
        <div class="card mb-4">
            <div class="card-header bg-secondary text-white">
                <h5 class="mb-0">${restaurant.name}</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <img src="${restaurant.image}" class="img-fluid rounded mb-3" alt="${restaurant.name}">
                        <img src="${restaurant.menuImage}" class="img-fluid rounded" alt="Menu">
                    </div>
                    <div class="col-md-6">
                        <h6 class="fw-bold">About</h6>
                        <p>${restaurant.description}</p>
                        
                        <div class="restaurant-info mb-3">
                            <div><i class="fas fa-utensils"></i> Cuisine: ${restaurant.cuisine}</div>
                            <div><i class="fas fa-clock"></i> Hours: ${restaurant.hours}</div>
                            <div><i class="fas fa-star text-warning"></i> Rating: ${restaurant.rating}</div>
                            <div><i class="fas fa-tag"></i> Price Range: ${restaurant.priceRange}</div>
                        </div>

                        <h6 class="fw-bold">Menu</h6>
                        <div class="menu-categories">
                            <div class="menu-category">
                                <h7>Starters</h7>
                                <ul class="list-unstyled">
                                    ${restaurant.menu.starters.map(item => 
                                        `<li>${item.name} <span class="price">€${item.price.toFixed(2)}</span></li>`
                                    ).join('')}
                                </ul>
                            </div>
                            <div class="menu-category">
                                <h7>Main Courses</h7>
                                <ul class="list-unstyled">
                                    ${restaurant.menu.mains.map(item => 
                                        `<li>${item.name} <span class="price">€${item.price.toFixed(2)}</span></li>`
                                    ).join('')}
                                </ul>
                            </div>
                            <div class="menu-category">
                                <h7>Desserts</h7>
                                <ul class="list-unstyled">
                                    ${restaurant.menu.desserts.map(item => 
                                        `<li>${item.name} <span class="price">€${item.price.toFixed(2)}</span></li>`
                                    ).join('')}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    document.getElementById('nearbyPlaces').innerHTML = detailsHtml;
}
}

function showNearbyList(activities, restaurants) {
    const modal = new bootstrap.Modal(document.getElementById('detailsModal'));
    let modalBodyContent = '';

    if (activities && activities.length > 0) {
        modalBodyContent += `<h4>Nearby Activities</h4><ul>`;
        activities.forEach(activity => {
            modalBodyContent += `<li>${activity.name}</li>`;
        });
        modalBodyContent += `</ul>`;
    }

    if (restaurants && restaurants.length > 0) {
        modalBodyContent += `<h4>Nearby Restaurants</h4><ul>`;
        restaurants.forEach(restaurant => {
            modalBodyContent += `<li>${restaurant.name}</li>`;
        });
        modalBodyContent += `</ul>`;
    }

    document.getElementById('modalBody').innerHTML = modalBodyContent;
    modal.show();
}

document.addEventListener('DOMContentLoaded', initMap);