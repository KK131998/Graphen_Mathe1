const graphInfoDiv = document.getElementById('graph-info');

const gewicht = graphInfoDiv.getAttribute('data-gewicht');
const richtung = graphInfoDiv.getAttribute('data-richtung');
const knoten = graphInfoDiv.getAttribute('data-knoten');

function fiftyFifty() {
    if (Math.random() < 0.5){
        return true
    } else {
        return false
    }
}

function zahlVonNullBisHundert(){
    console.log(Math.floor(Math.random() * 101));
    return Math.floor(Math.random() * 101)
}

function adjajenzmatrix(gewicht, richtung, knoten) {
    let edges = [];

    const resultContainer = document.createElement('div');
    resultContainer.className = 'result';
    resultContainer.id = 'result-container';

    // Inhalte dynamisch erstellen
    const heading = document.createElement('h2');
    heading.textContent = 'Adjazenzmatrix';

    // Tabelle erstellen
    const table = document.createElement('table');

    // Tabellenüberschrift
    const headerRow = document.createElement('tr');
    const headerCell = document.createElement('th');
    headerCell.textContent = ''; // Leere Zelle für die Ecke
    headerRow.appendChild(headerCell);
    for (let i = 1; i <= knoten; i++) {
        const th = document.createElement('th');
        th.textContent = ` ${i}`;
        headerRow.appendChild(th);
    }
    table.appendChild(headerRow);

    // Ungewichtet und Ungerichtet
    if (gewicht === "ungewichtet" && richtung === 'ungerichtet'){
        for (let i = 1; i <= knoten; i++) {
            const row = document.createElement('tr');
            const rowHeader = document.createElement('th');
            rowHeader.textContent = `${i}`;
            row.appendChild(rowHeader);
            // Innere Schleife für die Spalten
            for (let j = 1; j <= knoten; j++) {
                const cell = document.createElement('td');
                const input = document.createElement('input'); // Eingabefeld erstellen
                input.id = 'knoten: ' + i + j;
                input.type = 'number'; // Typ auf Zahl setzen
                input.value = 0; // Standardwert setzen
                input.min = '0'; // Minimalwert setzen (optional)
                input.max = '1';

                // Diagonale Eingabefelder deaktivieren
                if (i === j || i > j) {
                   input.disabled = true;
                   input.style.backgroundColor = '#e9ecef';
                }   else {
                    // Event-Listener für die Felder oberhalb der Diagonalen
                    input.addEventListener('blur', function() {
                        // Gegenüberliegendes Feld finden
                        const oppositeInput = document.getElementById(`knoten: ${j}${i}`);
                        if (oppositeInput) {
                            oppositeInput.value = input.value; // Wert synchronisieren
                        }
                    });
                }

                cell.appendChild(input); // Eingabefeld in die Zelle einfügen
                row.appendChild(cell);
            }
            table.appendChild(row);
        }
    }

    // Gewichtet und Ungerichtet
    else if (gewicht === "gewichtet" && richtung === 'ungerichtet'){
        for (let i = 1; i <= knoten; i++) {
            const row = document.createElement('tr');
            const rowHeader = document.createElement('th');
            rowHeader.textContent = `${i}`;
            row.appendChild(rowHeader);
            // Innere Schleife für die Spalten
            for (let j = 1; j <= knoten; j++) {
                const cell = document.createElement('td');
                const input = document.createElement('input'); // Eingabefeld erstellen
                input.id = 'knoten: ' + i + j;
                input.type = 'number'; // Typ auf Zahl setzen
                input.value = 0; // Standardwert setzen
                input.min = '-1000'; // Minimalwert setzen (optional)

                // Diagonale Eingabefelder deaktivieren
                if (i === j || i > j) {
                   input.disabled = true;
                   input.style.backgroundColor = '#e9ecef';
                }   else {
                    // Event-Listener für die Felder oberhalb der Diagonalen
                    input.addEventListener('click', function() {
                        // Gegenüberliegendes Feld finden
                        const oppositeInput = document.getElementById(`knoten: ${j}${i}`);
                        if (oppositeInput) {
                            oppositeInput.value = input.value; // Wert synchronisieren
                        }
                    });
                }

                cell.appendChild(input); // Eingabefeld in die Zelle einfügen
                row.appendChild(cell);
            }
            table.appendChild(row);
        }
    }

// Ungewichtet und Gerichtet
    else if (gewicht === "ungewichtet" && richtung === 'gerichtet'){
        for (let i = 1; i <= knoten; i++) {
            const row = document.createElement('tr');
            const rowHeader = document.createElement('th');
            rowHeader.textContent = `${i}`;
            row.appendChild(rowHeader);
            // Innere Schleife für die Spalten
            for (let j = 1; j <= knoten; j++) {
                const cell = document.createElement('td');
                const input = document.createElement('input'); // Eingabefeld erstellen
                input.id = 'knoten: ' + i + j;
                input.type = 'number'; // Typ auf Zahl setzen
                input.value = 0; // Standardwert setzen
                input.min = '0'; // Minimalwert setzen (optional)
                input.max = '1'; // Minimalwert setzen (optional)

                // Diagonale Eingabefelder deaktivieren
                if (i === j) {
                input.disabled = true;
                input.style.backgroundColor = '#e9ecef';
                }

                cell.appendChild(input); // Eingabefeld in die Zelle einfügen
                row.appendChild(cell);
            }
            table.appendChild(row);
        }
    }


// Ungewichtet und Gerichtet
    else if (gewicht === "gewichtet" && richtung === 'gerichtet'){
        for (let i = 1; i <= knoten; i++) {
            const row = document.createElement('tr');
            const rowHeader = document.createElement('th');
            rowHeader.textContent = `${i}`;
            row.appendChild(rowHeader);
            // Innere Schleife für die Spalten
            for (let j = 1; j <= knoten; j++) {
                const cell = document.createElement('td');
                const input = document.createElement('input'); // Eingabefeld erstellen
                input.id = 'knoten: ' + i + j;
                input.type = 'number'; // Typ auf Zahl setzen
                input.value = 0; // Standardwert setzen

                // Diagonale Eingabefelder deaktivieren
                if (i === j) {
                input.disabled = true;
                input.style.backgroundColor = '#e9ecef';
                }

                cell.appendChild(input); // Eingabefeld in die Zelle einfügen
                row.appendChild(cell);
            }
            table.appendChild(row);
        }
    }

    const kreiereGraph = document.createElement('button');
    const zufallButton = document.createElement('button');
    kreiereGraph.textContent = 'Graph kreieren'; // Button-Text
    zufallButton.textContent = 'Zufällig ausfüllen'; // Button-Text

    kreiereGraph.addEventListener('click', function() {
        // Passendes Array zum erstellen des Graphen schaffen 
        if (gewicht === "ungewichtet" && richtung === 'ungerichtet'){
            let zaehler = 0;
            for (var i = 1; i <= knoten; i++){
                for (var j = 1; j <= knoten; j++) {
                    if (parseInt(document.getElementById('knoten: ' + i + j).value) === 1){
                    edges[zaehler] = [i, j];
                    zaehler++;
                    }
                }
            }
        }

        // Passendes Array zum erstellen des Graphen schaffen 
        else if (gewicht === "gewichtet" && richtung === 'ungerichtet'){
            let zaehler = 0;
            for (var i = 1; i <= knoten; i++){
                for (var j = 1; j <= knoten; j++) {
                    if (parseInt(document.getElementById('knoten: ' + i + j).value) !== 0) {
                        edges[zaehler] = [i, j, document.getElementById('knoten: ' + i + j).value];
                        zaehler++;
                    }
                }
            }
        }

        // Passendes Array zum erstellen des Graphen schaffen 
        else if (gewicht === "ungewichtet" && richtung === 'gerichtet'){
            let zaehler = 0;
            for (var i = 1; i <= knoten; i++){
                for (var j = 1; j <= knoten; j++) {
                    if (parseInt(document.getElementById('knoten: ' + i + j).value) === 1){
                        edges[zaehler] = [i, j];
                    zaehler++;
                    }
                }
            }
        }

        // Passendes Array zum erstellen des Graphen schaffen 
        else if (gewicht === "gewichtet" && richtung === 'gerichtet'){
            let zaehler = 0;
            for (var i = 1; i <= knoten; i++){
                for (var j = 1; j <= knoten; j++) {
                    if (parseInt(document.getElementById('knoten: ' + i + j).value) !== 0) {
                        edges[zaehler] = [i, j, document.getElementById('knoten: ' + i + j).value];
                        zaehler++;

                    }
                }
            }
        }

        fetch('/submit-edges', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ edges: edges }) // Sende die Kanten als JSON
        })
        .then(response => {
            if (response.ok) {
                return response.json(); // Warte auf die JSON-Antwort des Servers
            } else {
                throw new Error('Netzwerkfehler beim Senden der Edges');
            }
        })
        .then(data => {
            console.log("Serverantwort:", data); // Ausgabe der Serverantwort
            // Optional: Weiterleitung nach erfolgreicher Anfrage
            window.location.href = '/graph'; // Weiterleitung zur graph.html Seite
        })
        .catch(error => {
            console.error("Fehler beim Senden der Edges:", error);
        });
    });

    zufallButton.addEventListener('click', function() {
        if (gewicht == 'ungewichtet' && richtung === 'gerichtet') {
            for (var i = 1; i <= knoten; i++){
                for (var j = 1; j <= knoten; j++) {
                    if (fiftyFifty ()){
                        document.getElementById('knoten: ' + i + j).value = 1;
                    } else {
                        document.getElementById('knoten: ' + i + j).value = 0;
                    }
                }
            }
        }
        else if (gewicht == 'gewichtet' && richtung === 'gerichtet') {
            for (var i = 1; i <= knoten; i++){
                for (var j = 1; j <= knoten; j++) {
                    if (fiftyFifty ()){
                        document.getElementById('knoten: ' + i + j).value = Math.floor(Math.random() * 101);
                    } else {
                        document.getElementById('knoten: ' + i + j).value = 0;
                    }
                }
            }
        }
        else if (gewicht == 'ungewichtet' && richtung === 'ungerichtet') {
            for (var i = 1; i <= knoten; i++){
                for (var j = 1; j <= knoten; j++) {
                    if (i < j){
                        if (fiftyFifty ()){
                            document.getElementById('knoten: ' + i + j).value = 1;
                            document.getElementById('knoten: ' + j + i).value = 1;
                        } else {
                            document.getElementById('knoten: ' + i + j).value = 0;
                        }
                    }
                }
            }
        }
        else if (gewicht == 'gewichtet' && richtung === 'ungerichtet') {
            for (var i = 1; i <= knoten; i++){
                for (var j = 1; j <= knoten; j++) {
                    if (i < j){
                        if (fiftyFifty ()){
                            let zahl1 = Math.floor(Math.random() * 101);
                            document.getElementById('knoten: ' + i + j).value = zahl1;
                            document.getElementById('knoten: ' + j + i).value = zahl1;
                        } else {
                            document.getElementById('knoten: ' + i + j).value = 0;
                        }
                    }
                }
            }
        }
    })




    
    // Inhalte in den Container einfügen
    resultContainer.appendChild(heading);
    resultContainer.appendChild(table);
    resultContainer.appendChild(kreiereGraph);
    resultContainer.appendChild(zufallButton);

    document.body.appendChild(resultContainer);
}

adjajenzmatrix(gewicht, richtung, knoten);

