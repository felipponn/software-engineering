/**
 * Classe que representa um manipulador de interface do usuário para várias interações.
 */
class UIHandler {
    constructor() {
        this.destinationRadios = document.getElementsByName('destination');
        this.machineInfo = document.getElementById('machineInfo');
        this.machineNumberInput = document.getElementById('machineNumber');
        this.filterSection = document.getElementById('filtersSection');
        this.toggleButton = document.getElementById('toggleFilters');
        this.filterTarget = document.getElementById('filterTarget');
        this.filterMachineContainer = document.getElementById('filterMachineContainer');
        this.filterMachine = document.getElementById('filterMachine');
        this.filterType = document.getElementById('filterType');
        this.filterStatus = document.getElementById('filterStatus');
        this.btnFilter = document.getElementById('btnFilter');
        this.btnReset = document.getElementById('btnReset');
        this.complaintsContainer = document.getElementById('complaintsContainer');

        // initialize handlers
         this.initDestinationHandler();
         this.initToggleFilters();
         this.initMachineFilterHandler();
         this.initSuccessMessageHandler();
         this.initFilterButtons();
 
        // update button texts with translations
        this.updateButtonTexts();
 
        // fetch and display complaints when the page loads
        this.fetchComplaints();
    }

    updateButtonTexts() {
        if (this.btnFilter) {
            this.btnFilter.textContent = translations.filter;
        }

        if (this.btnReset) {
            this.btnReset.textContent = translations.reset_filters;
        }
    }

    /**
     * Initializes the destination selection handler.
     */
    initDestinationHandler() {
        if (this.destinationRadios) {
            this.destinationRadios.forEach(radio => {
                radio.addEventListener('change', this.handleRadioChange.bind(this));
            });

            // check the initial state
            const selectedRadio = document.querySelector('input[name="destination"]:checked');
            if (selectedRadio) {
                this.handleRadioChange({ target: selectedRadio });
            }
        }
    }

    /**
     * Handles the change in the radio button selection.
     * @param {Event} event - The event triggered when changing the radio button.
     */
    handleRadioChange(event) {
        const selectedRadio = event.target;
        if (selectedRadio.value === 'machine' && selectedRadio.checked) {
            this.showMachineInfo();
        } else if (selectedRadio.value === 'app' && selectedRadio.checked) {
            this.hideMachineInfo();
        }
    }

    /**
     * Displays the machine information section.
     */
    showMachineInfo() {
        this.machineInfo.style.display = 'block';
        this.machineNumberInput.setAttribute('required', 'required');
    }

    /**
     * Hides the machine information section.
     */
    hideMachineInfo() {
        this.machineInfo.style.display = 'none';
        this.machineNumberInput.removeAttribute('required');
    }

    /**
     * Initializes the toggle filters button.
     */
    initToggleFilters() {
        if (this.toggleButton) {
            this.toggleButton.addEventListener('click', this.toggleFilters.bind(this));
        }
    }

    /**
     * Toggles the visibility of the filter section.
     */
    toggleFilters() {
        if (this.filterSection) {
            const isHidden = this.filterSection.classList.toggle('hidden');
            this.filterSection.classList.toggle('visible', !isHidden);
            this.toggleButton.innerHTML = isHidden 
                ? `<i class="fas fa-filter"></i> ${translations.show_filters}` 
                : `<i class="fas fa-filter"></i> ${translations.hide_filters}`;
        }
    }

    /**
     * Initializes the machine filter handler.
     */
    initMachineFilterHandler() {
        if (this.filterTarget && this.filterMachineContainer) {
            this.toggleMachineFilter();
            this.filterTarget.addEventListener('change', this.toggleMachineFilter.bind(this));
        }
    }

    /**
     * Toggles the visibility of the machine filter based on the selected target.
     */
    toggleMachineFilter() {
        if (this.filterTarget.value === 'machine') {
            this.filterMachineContainer.style.display = 'block';
        } else {
            this.filterMachineContainer.style.display = 'none';
            this.filterMachine.value = 'all'; // Resetar o valor ao ocultar
        }
    }

    /**
     * Initializes the success message handler to hide after 5 seconds.
     */
    initSuccessMessageHandler() {
        const successMessage = document.querySelector('.successMessage');
        if (successMessage) {
            setTimeout(() => {
                successMessage.style.transition = 'opacity 1s';
                successMessage.style.opacity = '0';
                setTimeout(() => {
                    successMessage.style.display = 'none';
                }, 1000);
            }, 5000);
        }
    }

    /**
     * Initializes the filter buttons.
     */
    initFilterButtons() {
        if (this.btnFilter) {
            this.btnFilter.addEventListener('click', () => {
                this.fetchComplaints();
            });
        }

        if (this.btnReset) {
            this.btnReset.addEventListener('click', () => {
                this.resetFilters();
                this.fetchComplaints();
            });
        }
    }

    /**
     * Resets the filter fields to their default values.
     */
    resetFilters() {
        this.filterTarget.value = 'all';
        this.filterMachine.value = 'all';
        this.filterType.value = 'all';
        this.filterStatus.value = 'all';
        this.toggleMachineFilter(); 
    }

    /**
     * Fetches the complaints from the server based on the filters and updates the interface.
     */
    fetchComplaints() {
        // Construir os parâmetros de consulta com base nos filtros
        const params = new URLSearchParams();

        if (this.filterTarget && this.filterTarget.value !== 'all') {
            params.append('target', this.filterTarget.value);
        }

        if (this.filterMachine && this.filterMachine.value !== 'all') {
            params.append('machine_id', this.filterMachine.value);
        }

        if (this.filterType && this.filterType.value !== 'all') {
            params.append('issue_type', this.filterType.value);
        }

        if (this.filterStatus && this.filterStatus.value !== 'all') {
            params.append('status', this.filterStatus.value);
        }

        // Mostrar um indicador de carregamento
        this.complaintsContainer.innerHTML = `<p>${translations.loading_complaints}</p>`;

        // Fazer a requisição ao servidor
        fetch(`/get_complaints?${params.toString()}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro na resposta da rede.');
                }
                return response.json();
            })
            .then(data => {
                this.displayComplaints(data);
            })
            .catch(error => {
                console.error('Erro ao buscar as reclamações:', error);
                this.complaintsContainer.innerHTML = `<p>${translations.error_fetching_complaints}</p>`;
            });
    }

    /**
     * Displays the complaints on the interface.
     * @param {Array} complaints - The list of complaints to be displayed.
     */
    displayComplaints(complaints) {
        // Limpar o container
        this.complaintsContainer.innerHTML = '';

        if (complaints.length === 0) {
            this.complaintsContainer.innerHTML = `<p>${translations.no_complaints_found}</p>`;
            return;
        }

        // Iterar sobre as reclamações e criar elementos
        complaints.forEach(complaint => {
            const complaintDiv = document.createElement('div');
            complaintDiv.classList.add('complaint');

            complaintDiv.innerHTML = `
                <h3>${translations.complaint} #${complaint.report_id}</h3>
                <p><strong>${translations.user_id}:</strong> ${complaint.user_id}</p>
                ${complaint.machine_id ? `<p><strong>${translations.machine_id}:</strong> ${complaint.machine_id}</p>` : ''}
                <p><strong>${translations.target}:</strong> ${complaint.report_target}</p>
                <p><strong>${translations.type}:</strong> ${complaint.issue_type}</p>
                <p><strong>${translations.description}:</strong> ${complaint.description}</p>
                <p class="status ${complaint.status === 'resolved' ? 'resolved' : 'unresolved'}">
                    <strong>${translations.status}:</strong> ${complaint.status}
                </p>
                <p><strong>${translations.created_at}:</strong> ${complaint.created_at}</p>
                ${complaint.resolved_at ? `<p><strong>${translations.resolved_at}:</strong> ${complaint.resolved_at}</p>` : ''}
            `;

            this.complaintsContainer.appendChild(complaintDiv);
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new UIHandler();
});