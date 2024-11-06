// This script handles the favorite icon on the machine profile page
// Future add new features

document.addEventListener('DOMContentLoaded', function() {
    const heartIcon = document.querySelector('.favorite-icon i');
    if (heartIcon) {
        heartIcon.addEventListener('click', function() {
            const machineId = this.getAttribute('data-machine-id');
            
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
                    alert(data.message || 'Ocorreu um erro.');
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                alert('Ocorreu um erro ao processar a solicitação.');
            });
        });
    }
});
