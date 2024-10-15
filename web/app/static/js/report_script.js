/**
 * Class to handle the display of machine information and the toggle of filter visibility.
 */
class UIHandler {
    /**
     * Constructor of the UIHandler class.
     * Initializes DOM elements and calls the init methods.
     */
    constructor() {
        // Elements related to machine information
        this.destinationRadios = document.getElementsByName('destination');
        this.machineInfo = document.getElementById('machineInfo');
        this.machineNumberInput = document.getElementById('machineNumber');
        
        // Elements related to filter toggling
        this.filtrosSection = document.getElementById('filtros-section');
        this.toggleButton = document.getElementById('toggle-filtros');
        
        // Initialize the functionalities
        this.initDestinationHandler();
        this.initToggleFilters();
    }

    /**
     * Initializes the destination selection handler.
     * Adds event listeners to the radio buttons to handle the selection change.
     */
    initDestinationHandler() {
        this.destinationRadios.forEach(radio => {
            radio.addEventListener('change', this.handleRadioChange.bind(this));
        });
    }

    /**
     * Handles the change of selection of the radio buttons.
     * Displays or hides the machine information based on the selection.
     * 
     * @param {Event} event - The event object containing the selected radio button.
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
     * Shows the machine information section and makes the machine number input required.
     */
    showMachineInfo() {
        this.machineInfo.style.display = 'block';
        this.machineNumberInput.setAttribute('required', 'required');
    }

    /**
     * Hides the machine information section and removes the required attribute from the machine number input.
     */
    hideMachineInfo() {
        this.machineInfo.style.display = 'none';
        this.machineNumberInput.removeAttribute('required');
    }

    /**
     * Initializes the filter toggle button.
     * Adds an event listener to the toggle button to handle the visibility of the filter section.
     */
    initToggleFilters() {
        this.toggleButton.addEventListener('click', this.toggleFiltros.bind(this));
    }

    /**
     * Toggles the visibility of the filter section and updates the button text accordingly.
     */
    toggleFiltros() {
        const isHidden = this.filtrosSection.classList.toggle('hidden');
        this.filtrosSection.classList.toggle('visible', !isHidden);

        this.toggleButton.innerHTML = isHidden ? '<i class="fas fa-filter"></i> Mostrar Filtros' : '<i class="fas fa-filter"></i> Esconder Filtros';
    }
}

// Initialize the UIHandler when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    new UIHandler();
});
