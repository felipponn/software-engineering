/**
 * Class representing a UI handler for various user interface interactions.
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
        this.initDestinationHandler();
        this.initToggleFilters();
        this.initMachineFilterHandler();
    }

    /**
     * Initializes the destination selection handler.
     */
    initDestinationHandler() {
        this.destinationRadios.forEach(radio => {
            radio.addEventListener('change', this.handleRadioChange.bind(this));
        });
    }

    /**
     * Handles the change of selection of the radio buttons.
     * @param {Event} event - The event triggered by changing a radio button.
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
     * Shows the machine information section.
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
     * Initializes the filter toggle button.
     */
    initToggleFilters() {
        this.toggleButton.addEventListener('click', this.toggleFilters.bind(this));
    }

    /**
     * Toggles the visibility of the filter section.
     */
    toggleFilters() {
        const isHidden = this.filterSection.classList.toggle('hidden');
        this.filterSection.classList.toggle('visible', !isHidden);
        this.toggleButton.innerHTML = isHidden ? '<i class="fas fa-filter"></i> Show Filters' : '<i class="fas fa-filter"></i> Hide Filters';
    }

    /**
     * Initializes the machine filter handler.
     */
    initMachineFilterHandler() {
        this.toggleMachineFilter();
        this.filterTarget.addEventListener('change', this.toggleMachineFilter.bind(this));
    }

    /**
     * Toggles the visibility of the machine filter based on the selected target.
     */
    toggleMachineFilter() {
        if (this.filterTarget.value === 'machine') {
            this.filterMachineContainer.style.display = 'block';
        } else {
            this.filterMachineContainer.style.display = 'none';
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new UIHandler();
});
