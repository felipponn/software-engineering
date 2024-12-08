/**
 * This script handles the stock manager page.
 * We are using javascript in this case only for being things from the frontend, 
 */
document.addEventListener('DOMContentLoaded', function() {
    // Get the necessary DOM elements for manipulation
    const stockContainer = document.getElementById('stockContainer');
    const filterMachine = document.getElementById('filterMachine');
    const filterProduct = document.getElementById('filterProduct');
    const filterQuantityCategory = document.getElementById('filterQuantityCategory');
    const btnFilter = document.getElementById('btnFilter');
    const btnReset = document.getElementById('btnReset');
    const toggleFilters = document.getElementById('toggleFilters');
    const filtersSection = document.getElementById('filtersSection');
    const granularity = document.getElementById('granularity');
    const operation = document.getElementById('operation');
    const applyStrategy = document.getElementById('applyStrategy');
    const stockSummaryTable = document.getElementById('stockSummaryTable');
    const stockSummaryBody = document.getElementById('stockSummaryBody');

    // Function to fetch stock data
    function fetchStock() {
        stockContainer.innerHTML = `<p>${translations.loading_stock}</p>`;
        let params = new URLSearchParams();
        // filters
        const machine_id = filterMachine.value !== 'all' ? filterMachine.value : null;
        const product_name = filterProduct.value !== 'all' ? filterProduct.value : null;
        const quantity_category = filterQuantityCategory.value !== 'all' ? filterQuantityCategory.value : null;

        if (machine_id) params.append('machine_id', machine_id);
        if (product_name) params.append('product_name', product_name);
        if (quantity_category) params.append('quantity_category', quantity_category);

        // Make the request to get stock data
        fetch(`/get_stock?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                stockContainer.innerHTML = '';
                if (data.length === 0) {
                    stockContainer.innerHTML = `<p>${translations.no_stock_found}</p>`;
                    return;
                }
        
                data.forEach(item => { // Iterate over the data and create elements for display
                    const stockDiv = document.createElement('div');
                    stockDiv.classList.add('stock-item');

                    // Add the quantity category class to the stockDiv
                    const categoryClass = item.quantity_category.toLowerCase(); 
                    stockDiv.classList.add(categoryClass);

                    stockDiv.innerHTML = `
                        <h3>${translations.product_name}: ${item.product_name}</h3>
                        <p><strong>${translations.machine_id}:</strong> ${item.machine_id}</p>
                        <p><strong>${translations.location}:</strong> ${item.location}</p>
                        <p><strong>${translations.quantity}:</strong> ${item.quantity}</p>
                        <p><strong>${translations.quantity_category}:</strong> ${item.quantity_category}</p>
                    `;
                    stockContainer.appendChild(stockDiv);
                });
            })
            .catch(error => {
                console.error('Error fetching stock data:', error); // Display error message in case of request failure
                stockContainer.innerHTML = `<p>${translations.error_fetching_stock}</p>`;
            });
    }

    // Function to fetch data for table
    function fetchTableData() {
        stockSummaryBody.innerHTML = '<tr><td colspan="4" style="text-align:center;">Nenhuma informação de estoque disponível</td></tr>';
        let params = new URLSearchParams();
        // filters
        const machine_id = filterMachine.value !== 'all' ? filterMachine.value : null;
        const product_name = filterProduct.value !== 'all' ? filterProduct.value : null;
        const quantity_category = filterQuantityCategory.value !== 'all' ? filterQuantityCategory.value : null;
        const granularity_value = granularity.value !== 'all' ? granularity.value : null;
        const operation_value = operation.value;

        if (machine_id) params.append('machine_id', machine_id);
        if (product_name) params.append('product_name', product_name);
        if (quantity_category) params.append('quantity_category', quantity_category);
        if (granularity_value) params.append('granularity', granularity_value);
        if (operation_value) params.append('operation', operation_value);

        // Make the request to get stock data
        fetch(`/get_stock?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                stockSummaryBody.innerHTML = '';
                if (data.length === 0) {
                    stockSummaryBody.innerHTML = '<tr><td colspan="4" style="text-align:center;">Nenhuma informação de estoque disponível</td></tr>';
                    return;
                }
        
                const tbody = document.createElement('tbody');
                
                data.forEach(item => { // Iterate over the data and create elements for display
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${item.machine_id}</td>
                        <td>${item.product_name}</td>
                        <td>${item.quantity}</td>
                        <td>${item.quantity_category}</td>
                    `;
                    tbody.appendChild(tr);
                });

                stockSummaryBody.innerHTML = tbody.innerHTML;
            })
            .catch(error => {
                console.error('Error fetching stock data:', error); // Display error message in case of request failure
                stockSummaryBody.innerHTML = '<tr><td colspan="4" style="text-align:center;">Nenhuma informação de estoque disponível</td></tr>';
            });
    }

    // Add click event for the filter button
    btnFilter.addEventListener('click', fetchStock);

    // Add click event for the reset filters button
    btnReset.addEventListener('click', () => {
        filterMachine.value = 'all';
        filterProduct.value = 'all';
        filterQuantityCategory.value = 'all';
        fetchStock();
    });

    // Add click event for the apply strategy button
    applyStrategy.addEventListener('click', fetchTableData);

    // Add click event to toggle the visibility of filters
    toggleFilters.addEventListener('click', () => {
        if (filtersSection.classList.contains('hidden')) {
            filtersSection.classList.remove('hidden');
            filtersSection.classList.add('visible');
            toggleFilters.innerHTML = `<i class="fas fa-filter"></i> ${translations.hide_filters}`;
        } else {
            filtersSection.classList.remove('visible');
            filtersSection.classList.add('hidden');
            toggleFilters.innerHTML = `<i class="fas fa-filter"></i> ${translations.show_filters}`;
        }
    });

    // Call the function to fetch stock data when the page loads
    fetchStock();
});
