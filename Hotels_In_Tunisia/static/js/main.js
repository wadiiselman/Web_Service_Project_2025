// Handle form submissions
document.addEventListener('DOMContentLoaded', function() {
    // Registration form handling
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            
            if (password !== confirmPassword) {
                e.preventDefault();
                alert('Passwords do not match!');
            }
        });
    }

    // Business profile updates
    const profileForm = document.getElementById('profileForm');
    if (profileForm) {
        profileForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(profileForm);
            
            fetch('/api/profile/update', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Profile updated successfully!');
                } else {
                    alert('Error updating profile');
                }
            });
        });
    }

    // Transportation calculator
    const transportForm = document.getElementById('transportForm');
    if (transportForm) {
        transportForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const from = document.getElementById('fromLocation').value;
            const to = document.getElementById('toLocation').value;
            
            fetch(`/api/transportation/options?from=${from}&to=${to}`)
                .then(response => response.json())
                .then(data => {
                    const resultsDiv = document.getElementById('transportResults');
                    resultsDiv.innerHTML = data.map(option => `
                        <div class="card mb-3">
                            <div class="card-body">
                                <h5>${option.means}</h5>
                                <p>Duration: ${option.duration} minutes</p>
                                <p>Price: ${option.price_estimate} TND</p>
                            </div>
                        </div>
                    `).join('');
                });
        });
    }
});

// Image preview functionality
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('imagePreview').src = e.target.result;
        }
        reader.readAsDataURL(input.files[0]);
    }
}

// Filter functionality
function filterItems(category) {
    document.querySelectorAll('.item-card').forEach(card => {
        if (category === 'all' || card.dataset.category === category) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}
