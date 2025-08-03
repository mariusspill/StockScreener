async function sendParam() {
    const pe = document.getElementById('pe').value;
    const pecheck = document.getElementById('cbpe').checked;
   
    const growthYears = document.getElementById('years').value;
    const growth = document.getElementById('growth').value;
    const growthcheck = document.getElementById('cbig').checked;

    const negative = document.getElementById('negative').checked;
    const volatility = document.getElementById('volatility').checked;

    var table = document.getElementById('resultTable');
    while (table.rows.length > 0) {
        table.deleteRow(0);
    }

    const response = await fetch('/screen', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ pe: pe,
                                pecheck: pecheck,
                                growthYears: growthYears,
                                growth: growth,
                                growthcheck: growthcheck,
                                negative: negative,
                                volatility: volatility
         })
    });

    if (response.ok) {
        const data = await response.json();
        var header = table.createTHead();
        var row = header.insertRow();

        var cell1 = document.createElement('th');
        cell1.innerText = "Ticker";

        var cell2 = document.createElement("th");
        cell2.innerText = "Growth rate"

        var cell3 = document.createElement("th");
        cell3.innerText = "PE"

        row.appendChild(cell1);
        row.appendChild(cell2);
        row.appendChild(cell3);
        for (const key in data){
            console.log(key, data[key]);


            var row = table.insertRow();
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);

            cell1.innerText = key;
            cell2.innerText = data[key][0];
            cell3.innerText = data[key][1];
        }
    } else {
        document.getElementById('result').innerText = 'Error fetching screening results';
    }
}