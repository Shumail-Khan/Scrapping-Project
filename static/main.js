function search() {
    const query = document.getElementById("query").value;

    document.getElementById("loading").classList.remove("d-none");
    document.getElementById("resultTable").classList.add("d-none");
    document.getElementById("download").classList.add("d-none");

    fetch("/search", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: query })
    })
    .then(res => res.json())
    .then(data => {
        const tbody = document.getElementById("tableBody");
        tbody.innerHTML = "";

        data.results.forEach(row => {
            tbody.innerHTML += `
                <tr>
                    <td>${row.source_name}</td>
                    <td>${row.text}</td>
                    <td>${row.timestamp}</td>
                </tr>
            `;
        });

        document.getElementById("loading").classList.add("d-none");
        document.getElementById("resultTable").classList.remove("d-none");

        const link = document.getElementById("csvLink");
        link.href = `/download/${data.csv_id}`;
        document.getElementById("download").classList.remove("d-none");
    });
}
