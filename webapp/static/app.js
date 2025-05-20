const form = document.getElementById('upload-form');
const tableBody = document.querySelector('#results-table tbody');

form.addEventListener('submit', async (event) => {
    event.preventDefault();
    tableBody.innerHTML = '';

    const fileInput = document.getElementById('image-input');
    const formData = new FormData();
    formData.append('image', fileInput.files[0]);

    const response = await fetch('/search', {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        const results = await response.json();
        results.forEach(result => {
            const row = document.createElement('tr');

            const previewCell = document.createElement('td');
            const img = document.createElement('img');
            img.src = result.thumbnail;
            img.className = 'preview';
            previewCell.appendChild(img);

            const linkCell = document.createElement('td');
            const a = document.createElement('a');
            a.href = result.url;
            a.textContent = result.url;
            linkCell.appendChild(a);

            row.appendChild(previewCell);
            row.appendChild(linkCell);
            tableBody.appendChild(row);
        });
    } else {
        alert('Erreur lors de la recherche.');
    }
});
