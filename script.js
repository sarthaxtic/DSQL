document.addEventListener('DOMContentLoaded', () => {
    const queryForm = document.getElementById('query-form');
    const queryInput = document.getElementById('query-input');
    const resultContainer = document.getElementById('result-container');
    const loadingSpinner = document.getElementById('loading-spinner');
    const queryResult = document.getElementById('query-result');
    const queryTable = document.getElementById('query-table');
    const tableHead = document.getElementById('query-table-head');
    const tableBody = document.getElementById('query-table-body');
    const queryPlot = document.getElementById('query-plot'); // For plot image

    queryForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Clear previous results
        queryResult.classList.add('d-none');
        queryTable.classList.add('d-none');
        queryPlot.classList.add('d-none');
        tableHead.innerHTML = '';
        tableBody.innerHTML = '';
        queryPlot.innerHTML = '';

        // Show loading spinner
        loadingSpinner.classList.remove('d-none');
        resultContainer.classList.remove('d-none');

        const query = queryInput.value.trim();

        try {
            const response = await fetch('http://127.0.0.1:5000/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Query failed');
            }

            // Show table if result exists
            if (data.result && data.result.length > 0) {
                const headers = Object.keys(data.result[0]);
                const rows = data.result.map(row => headers.map(h => row[h]));
                renderTable(headers, rows);
                queryTable.classList.remove('d-none');
            }

            // Show plot if exists
            if (data.plot) {
                const img = document.createElement('img');
                img.src = `data:image/png;base64,${data.plot}`;
                img.alt = 'Query Plot';
                img.className = 'img-fluid';
                queryPlot.appendChild(img);
                queryPlot.classList.remove('d-none');
            }

            if ((!data.result || data.result.length === 0) && !data.plot) {
                queryResult.textContent = 'No results returned.';
                queryResult.classList.remove('d-none');
            }

        } catch (error) {
            queryResult.textContent = `Error: ${error.message}`;
            queryResult.classList.remove('d-none');
        } finally {
            loadingSpinner.classList.add('d-none');
        }
    });

    function renderTable(headers, rows) {
        const headerRow = document.createElement('tr');
        headers.forEach(header => {
            const th = document.createElement('th');
            th.textContent = header;
            headerRow.appendChild(th);
        });
        tableHead.appendChild(headerRow);

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
