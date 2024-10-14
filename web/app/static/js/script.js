const destinationRadios = document.getElementsByName('destination');

destinationRadios.forEach(radio => {
    radio.addEventListener('change', () => {
        if (radio.value === 'machine' && radio.checked) {
            machineInfo.style.display = 'block';
            machineNumberInput.setAttribute('required', 'required');
        } else if (radio.value === 'app' && radio.checked) {
            machineInfo.style.display = 'none';
            machineNumberInput.removeAttribute('required');
        }
    });
});