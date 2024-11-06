
// Start of Selection

document.addEventListener('DOMContentLoaded', function() {
    const heartIcon = document.querySelector('.favorite-icon i');
    if (heartIcon) {
        heartIcon.addEventListener('click', function() {
            const machineId = this.getAttribute('data-machine-id');
            const isFavorite = this.classList.contains('favorite');
            
            fetch(`/toggle_favorite/${machineId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (data.is_favorite) {
                        this.classList.remove('far', 'not-favorite');
                        this.classList.add('fas', 'favorite');
                    } else {
                        this.classList.remove('fas', 'favorite');
                        this.classList.add('far', 'not-favorite');
                    }
                } else {
                    alert(data.message || 'An error occurred.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while processing the request.');
            });
        });
    }
});