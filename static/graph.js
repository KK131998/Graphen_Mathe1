
const dijkstra_button = document.getElementById("dijkstra_button");
dijkstra_button.addEventListener("click", function() {
    console.log("Dijkstra-Button wurde gedrückt");

    var dijkstra_knoten = [document.getElementById("Startknoten").value, document.getElementById("Endknoten").value];
    fetch('/submit-dijkstra', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ dijkstra_knoten: dijkstra_knoten }) // Sende die Kanten als JSON
    })
    .then(response => {
        if (response.ok) {
            return response.json(); // Warte auf die JSON-Antwort des Servers
        } else {
            document.getElementById("kuerzester-weg").innerHTML = 'Unerreichbar';
            throw new Error('Netzwerkfehler beim Senden der Edges');
        }
    })
    .then(data => {
        console.log("Serverantwort:", data); // Ausgabe der Serverantwort
        // Optional: Weiterleitung nach erfolgreicher Anfrage
        const kuerzesterWeg = data.kuerzesterWeg;
        console.log("Kürzester Weg:", kuerzesterWeg);

        // Kuerzesten Weg zeigen
        document.getElementById("kuerzester-weg").innerHTML = kuerzesterWeg;
    })
    .catch(error => {
        console.error("Fehler beim Senden der Edges:", error);
    });
});

