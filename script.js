document.addEventListener('DOMContentLoaded', () => {
    const queryForm = document.getElementById('query-form');
    const queryInput = document.getElementById('query-input');
    const resultContainer = document.getElementById('result-container');
    const loadingSpinner = document.getElementById('loading-spinner');
    const queryResult = document.getElementById('query-result');
    const queryTable = document.getElementById('query-table');
    const tableHead = document.getElementById('query-table-head');
    const tableBody = document.getElementById('query-table-body');

    queryForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Clear previous results
        queryResult.classList.add('d-none');
        queryTable.classList.add('d-none');
        tableHead.innerHTML = '';
        tableBody.innerHTML = '';

        // Show loading spinner
        loadingSpinner.classList.remove('d-none');
        resultContainer.classList.remove('d-none');

        const query = queryInput.value.trim();

        try {
            // Send query to Flask backend
            const response = await fetch('http://127.0.0.1:5000/execute_query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();

            if (data.type === 'text') {
                queryResult.textContent = data.data;
                queryResult.classList.remove('d-none');
            } else if (data.type === 'table') {
                renderTable(data.data);
                queryTable.classList.remove('d-none');
            }
        } catch (error) {
            queryResult.textContent = `Error: ${error.message}`;
            queryResult.classList.remove('d-none');
        } finally {
            loadingSpinner.classList.add('d-none');
        }
    });

    function renderTable(data) {
        const { headers, rows } = data;

        // Render table headers
        const headerRow = document.createElement('tr');
        headers.forEach(header => {
            const th = document.createElement('th');
            th.textContent = header;
            headerRow.appendChild(th);
        });
        tableHead.appendChild(headerRow);

        // Render table rows
        rows.forEach(row => {
            const tr = document.createElement('tr');
            row.forEach(cell => {
                const td = document.createElement('td');
                td.textContent = cell;
                tr.appendChild(td);
            });
            tableBody.appendChild(tr);
        });
    }
});
