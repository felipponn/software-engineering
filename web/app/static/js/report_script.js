/**
 * Classe que representa um manipulador de interface do usuário para várias interações.
 */
class UIHandler {
    constructor() {
        // Referências aos elementos do DOM
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

        // Inicializar manipuladores
        this.initDestinationHandler();
        this.initToggleFilters();
        this.initMachineFilterHandler();
        this.initSuccessMessageHandler();
        this.initFilterButtons();

        // Buscar e exibir reclamações ao carregar a página
        this.fetchComplaints();
    }

    /**
     * Inicializa o manipulador de seleção de destino.
     */
    initDestinationHandler() {
        if (this.destinationRadios) {
            this.destinationRadios.forEach(radio => {
                radio.addEventListener('change', this.handleRadioChange.bind(this));
            });

            // Verificar o estado inicial
            const selectedRadio = document.querySelector('input[name="destination"]:checked');
            if (selectedRadio) {
                this.handleRadioChange({ target: selectedRadio });
            }
        }
    }

    /**
     * Manipula a mudança de seleção dos botões de rádio.
     * @param {Event} event - O evento disparado ao mudar o botão de rádio.
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
     * Exibe a seção de informações da máquina.
     */
    showMachineInfo() {
        this.machineInfo.style.display = 'block';
        this.machineNumberInput.setAttribute('required', 'required');
    }

    /**
     * Oculta a seção de informações da máquina.
     */
    hideMachineInfo() {
        this.machineInfo.style.display = 'none';
        this.machineNumberInput.removeAttribute('required');
    }

    /**
     * Inicializa o botão de alternar filtros.
     */
    initToggleFilters() {
        if (this.toggleButton) {
            this.toggleButton.addEventListener('click', this.toggleFilters.bind(this));
        }
    }

    /**
     * Alterna a visibilidade da seção de filtros.
     */
    toggleFilters() {
        if (this.filterSection) {
            const isHidden = this.filterSection.classList.toggle('hidden');
            this.filterSection.classList.toggle('visible', !isHidden);
            this.toggleButton.innerHTML = isHidden ? '<i class="fas fa-filter"></i> Mostrar Filtros' : '<i class="fas fa-filter"></i> Esconder Filtros';
        }
    }

    /**
     * Inicializa o manipulador do filtro de máquina.
     */
    initMachineFilterHandler() {
        if (this.filterTarget && this.filterMachineContainer) {
            this.toggleMachineFilter();
            this.filterTarget.addEventListener('change', this.toggleMachineFilter.bind(this));
        }
    }

    /**
     * Alterna a visibilidade do filtro de máquina com base no alvo selecionado.
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
     * Inicializa o manipulador da mensagem de sucesso para ocultar após 5 segundos.
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
     * Inicializa os botões de filtro.
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
     * Reseta os campos de filtro para seus valores padrão.
     */
    resetFilters() {
        this.filterTarget.value = 'all';
        this.filterMachine.value = 'all';
        this.filterType.value = 'all';
        this.filterStatus.value = 'all';
        this.toggleMachineFilter(); // Garantir que o filtro de máquina esteja oculto
    }

    /**
     * Busca as reclamações do servidor com base nos filtros e atualiza a interface.
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

        // Mostrar um indicador de carregamento, se desejar
        this.complaintsContainer.innerHTML = '<p>Carregando reclamações...</p>';

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
                this.complaintsContainer.innerHTML = '<p>Ocorreu um erro ao buscar as reclamações.</p>';
            });
    }

    /**
     * Exibe as reclamações na interface.
     * @param {Array} complaints - A lista de reclamações a serem exibidas.
     */
    displayComplaints(complaints) {
        // Limpar o container
        this.complaintsContainer.innerHTML = '';

        if (complaints.length === 0) {
            this.complaintsContainer.innerHTML = '<p>Nenhuma reclamação encontrada.</p>';
            return;
        }

        // Iterar sobre as reclamações e criar elementos
        complaints.forEach(complaint => {
            const complaintDiv = document.createElement('div');
            complaintDiv.classList.add('complaint');

            complaintDiv.innerHTML = `
                <h3>Reclamação #${complaint.report_id}</h3>
                <p><strong>Usuário ID:</strong> ${complaint.user_id}</p>
                ${complaint.machine_id ? `<p><strong>Máquina ID:</strong> ${complaint.machine_id}</p>` : ''}
                <p><strong>Alvo:</strong> ${complaint.report_target}</p>
                <p><strong>Tipo:</strong> ${complaint.issue_type}</p>
                <p><strong>Descrição:</strong> ${complaint.description}</p>
                <p class="status ${complaint.status === 'resolved' ? 'resolved' : 'unresolved'}">
                    <strong>Status:</strong> ${complaint.status}
                </p>
                <p><strong>Criado em:</strong> ${complaint.created_at}</p>
                ${complaint.resolved_at ? `<p><strong>Resolvido em:</strong> ${complaint.resolved_at}</p>` : ''}
            `;

            this.complaintsContainer.appendChild(complaintDiv);
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new UIHandler();
});
