let gewicht = document.getElementById('gewicht')
let richtung = document.getElementById('richtung')
let knoten = document.getElementById('knoten')

let zufallsbutton = document.getElementById('zufall')

zufallsbutton.addEventListener('click', () => {
    let zufallszahl_gewicht = Math.floor(Math.random() * 100)
    let zufallszahl_richtung = Math.floor(Math.random() * 100)
    let zufallszahl_knoten = Math.floor(Math.random() * (10 - 4) + 4);

    if (zufallszahl_gewicht < 50) {
        gewicht.value = 'gewichtet';
    }
    else {
        gewicht.value = 'ungewichtet';
    }

    if (zufallszahl_richtung < 50) {
        richtung.value = 'gerichtet';
    }
    else {
        richtung.value = 'ungerichtet';
    }

    knoten.value = zufallszahl_knoten;
})
