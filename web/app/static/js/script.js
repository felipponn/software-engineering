/**
 * Class to handle the display of machine information based on the destination selection.
 */
class DestinationHandler {
    /**
     * Constructor of the DestinationHandler class.
     * Initializes DOM elements and calls the init method.
     */
    constructor() {
        this.destinationRadios = document.getElementsByName('destination');
        this.machineInfo = document.getElementById('machineInfo');
        this.machineNumberInput = document.getElementById('machineNumber');
        this.init();
    }

    /**
     * Adds event listeners to the radio buttons to handle the selection change.
     */
    init() {
        this.destinationRadios.forEach(radio => {
            radio.addEventListener('change', () => this.handleRadioChange(radio));
        });
    }

    /**
     * Handles the change of selection of the radio buttons.
     * Displays or hides the machine information based on the selection.
     * 
     * @param {HTMLInputElement} radio - The radio button that was selected.
     */
    handleRadioChange(radio) {
        if (radio.value === 'machine' && radio.checked) {
            this.machineInfo.style.display = 'block';
            this.machineNumberInput.setAttribute('required', 'required');
        } else if (radio.value === 'app' && radio.checked) {
            this.machineInfo.style.display = 'none';
            this.machineNumberInput.removeAttribute('required');
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new DestinationHandler();
});