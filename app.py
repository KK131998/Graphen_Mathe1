from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
from flask_cors import CORS  # Importiere 
import networkx as nx #graphen erstellen und verändern
import matplotlib.pyplot as plt #Graphen darstellen
import matplotlib
import os

app = Flask(__name__)
CORS(app)  # Aktiviere CORS für alle Routen

# Pfad zum Speichern der Bilder
IMAGE_PATH = './static/images'

# Stelle sicher, dass das Verzeichnis existiert
if not os.path.exists(IMAGE_PATH):
    os.makedirs(IMAGE_PATH)

# Überprüfen und Erstellen des Verzeichnisses, wenn es nicht existiert
if not os.path.exists('./images'):
    os.makedirs('./images')

class GraphState:
    def __init__(self):
        self.gewicht = 'ungewichtet'
        self.richtung = 'ungerichtet'
        self.knoten = None
        self.edges = None
        self.vollständigkeit = None
        self.eulerkreis = None
        self.hamiltonkreis = None
        self.art = None
        
graph_state = GraphState()

#ROUTEN:
@app.route('/')
def home():
    return render_template('index.html')  # Render die index.html-Seite

@app.route('/matrix', methods=['POST'])
def matrix():
    graph_state.gewicht = request.form.get('gewicht')
    graph_state.richtung = request.form.get('richtung')
    graph_state.knoten = request.form.get('knoten')
    return render_template('matrix.html', gewicht=graph_state.gewicht, richtung=graph_state.richtung, knoten=graph_state.knoten) 


@app.route('/submit-edges', methods=['POST'])
def submit_edges():
    data = request.get_json()  # JSON-Daten vom Client empfangen
    
    #edges anpassen
    edges_liste = data.get('edges')  # Das 'edges'-Array extrahieren
    edges = [tuple(edge) for edge in edges_liste]
    
    #knoten anpassen
    knoten = int(graph_state.knoten)
    knoten = list(range(1, knoten + 1))

    print("Erhaltene Edges:", edges, type(edges))
    print("Erhaltene Gewicht:", graph_state.gewicht) 
    print("Erhaltene Richtung:", graph_state.richtung) 
    print("Erhaltene Knoten:", knoten, type(knoten)) 
    
    # Graphen erstellen und Pfad des gespeicherten Graphenbildes erhalten
    graphErstellen(graph_state.gewicht, graph_state.richtung, knoten, edges)
    
    # Sicherstellen, dass die Antwort im richtigen Format erfolgt
    return jsonify({"message": "Graph erfolgreich erstellt"})

# Route, um das Bild über den Webserver zugänglich zu machen
@app.route('/static/images/<filename>')
def send_image(filename):
    return send_from_directory(IMAGE_PATH, filename)

@app.route('/graph')
def graph():
    return render_template('graph.html', vollständigkeit=graph_state.vollständigkeit, eulerkreis=graph_state.eulerkreis, hamiltonkreis=graph_state.hamiltonkreis, art=graph_state.art)



#FUNKTIONEN:

# Überprüfen, ob der Graph vollständig ist
def is_complete_graph_ungerichtet(G):
    anzahl_knoten = len(G.nodes)
    
    #Berechnen der maxmalen Anzahl an Kanten in dem Graphenh anhand der Anzahl der Knoten
    max_anzahl_kanten = anzahl_knoten * (anzahl_knoten - 1) // 2
    #Überprüfen ob die Kanten des Graphen gleich der maxmalen möglichen Anzahl an Kanten ist
    if len(G.edges) != max_anzahl_kanten:
        return False
    else:
        return True 

def is_complete_graph_gerichtet(G):
    anzahl_knoten = len(G.nodes)
    
    #Berechnen der maxmalen Anzahl an Kanten in dem Graphenh anhand der Anzahl der Knoten
    max_anzahl_kanten = anzahl_knoten * (anzahl_knoten - 1)
    #Überprüfen ob die Kanten des Graphen gleich der maxmalen möglichen Anzahl an Kanten ist
    if len(G.edges) != max_anzahl_kanten:
        return False
    else:
        return True 

# Überprüfen, ob der Hamilton-Kreis vorliegt, dieser teil des hamilton überprüfung funktioniert für gerichtet und ungerichtet
def is_hamiltonian_cycle(graph, cycle):
    """Überprüft, ob der gegebene Zyklus ein Hamiltonkreis ist"""
    # Ein Hamiltonkreis muss alle Knoten einmal besuchen und zurück zum Startknoten gehen
    if len(cycle) != len(graph.nodes):  # Der Zyklus muss alle Knoten enthalten
        return False
    
    # Überprüfen, ob der Zyklus alle Kanten enthält
    for i in range(len(cycle)):
        if not graph.has_edge(cycle[i], cycle[(i + 1) % len(cycle)]):
            return False  # Es gibt keine Kante zwischen den Knoten im Zyklus
    return True

# Überprüfen, ob der Hamilton-Kreis vorliegt
def find_hamiltonian_cycle_ungerichtet(graph):
    """Versucht, einen Hamiltonkreis in einem unvollständigen Graphen zu finden"""
    nodes = list(graph.nodes)
    
    def backtrack(current_path):
        # Wenn der aktuelle Pfad alle Knoten enthält und es eine Kante zum ersten Knoten gibt
        if len(current_path) == len(nodes):
            if graph.has_edge(current_path[-1], current_path[0]):
                return current_path + [current_path[0]]  # Ein Hamiltonkreis ist gefunden
            else:
                return None
        
        # Versuche, einen weiteren Knoten hinzuzufügen
        for node in nodes:
            if node not in current_path and (len(current_path) == 0 or graph.has_edge(current_path[-1], node)):
                result = backtrack(current_path + [node])
                if result is not None:
                    return result
        return None
    
    # Starte den Backtracking-Algorithmus von jedem möglichen Knoten
    for node in nodes:
        cycle = backtrack([node])
        if cycle is not None:
            return cycle  # Ein Hamiltonkreis wurde gefunden
    
    return None  # Kein Hamiltonkreis gefunden

def find_hamiltonian_cycle_gerichtet(graph):
    """Versucht, einen Hamiltonkreis in einem gerichteten oder ungerichteten Graphen zu finden"""
    nodes = list(graph.nodes)
    
    def backtrack(current_path):
        # Wenn der aktuelle Pfad alle Knoten enthält und es eine Kante zum ersten Knoten gibt
        if len(current_path) == len(nodes):
            if graph.has_edge(current_path[-1], current_path[0]):  # Richtung wird hier überprüft
                return current_path + [current_path[0]]  # Ein Hamiltonkreis ist gefunden
            else:
                return None
        
        # Versuche, einen weiteren Knoten hinzuzufügen
        for node in nodes:
            if node not in current_path and graph.has_edge(current_path[-1], node):  # Richtung prüfen
                result = backtrack(current_path + [node])
                if result is not None:
                    return result
        return None
    
    # Starte den Backtracking-Algorithmus von jedem möglichen Knoten
    for node in nodes:
        cycle = backtrack([node])
        if cycle is not None:
            return cycle  # Ein Hamiltonkreis wurde gefunden
    
    return None  # Kein Hamiltonkreis gefunden

def is_ring_graph_ungerichtet(G):
    # Schritt 1: Überprüfen, ob der Graph zusammenhängend ist
    if not nx.is_connected(G):
        return False
    
    # Schritt 2: Überprüfen der Gradzahl
    for node in G.nodes:
        if G.degree(node) != 2:
            return False

    # Schritt 3: Überprüfen, ob es genau einen Zyklus gibt
    # Ein Ring ist zyklenfrei und hat genau n Kanten, wobei n die Anzahl der Knoten ist
    if G.number_of_edges() != len(G.nodes):
        return False

    # Wenn alle Prüfungen bestanden sind, handelt es sich um einen Ring
    return True

def is_ring_graph_gerichtet(G):
    if isinstance(G, nx.DiGraph):  # Für gerichtete Graphen
        # Prüfe, ob der Graph ein starker gerichteter Zyklus ist
        if nx.is_strongly_connected(G) and all(G.out_degree(n) == 1 and G.in_degree(n) == 1 for n in G.nodes):
            return True
    else:  # Für ungerichtete Graphen
        if nx.is_connected(G) and all(G.degree(n) == 2 for n in G.nodes) and G.number_of_edges() == len(G.nodes):
            return True
    
    return False

def is_stern_graph_ungerichtet(G):
    # Der Graph muss zusammenhängend sein
    if not nx.is_connected(G):
        return False

    # Es muss genau einen Knoten mit Grad n-1 geben (der zentrale Knoten)
    # und alle anderen Knoten müssen Grad 1 haben
    degrees = [G.degree(node) for node in G.nodes]
    
    # Ein Stern-Graph hat genau einen Knoten mit Grad n-1 und alle anderen Knoten haben Grad 1
    if degrees.count(len(G.nodes) - 1) == 1 and degrees.count(1) == len(G.nodes) - 1:
        return True
    
    return False

def is_stern_graph_gerichtet(G):
    if not nx.is_connected(G.to_undirected()):  # Für gerichtete Graphen muss die ungerichtete Version zusammenhängend sein
        return False
    
    degrees = [(G.in_degree(n), G.out_degree(n)) for n in G.nodes]
    if isinstance(G, nx.DiGraph):  # Für gerichtete Graphen
        # Prüfen auf Einzugs- oder Aussendungsstern
        in_degrees = [deg[0] for deg in degrees]
        out_degrees = [deg[1] for deg in degrees]
        if in_degrees.count(len(G.nodes) - 1) == 1 and out_degrees.count(0) == len(G.nodes) - 1:
            return True  # Einzugsstern
        if out_degrees.count(len(G.nodes) - 1) == 1 and in_degrees.count(0) == len(G.nodes) - 1:
            return True  # Aussendungsstern
    else:  # Für ungerichtete Graphen
        return degrees.count(len(G.nodes) - 1) == 1 and degrees.count(1) == len(G.nodes) - 1
    
    return False

def art_des_Graphen_finden(G):
    if isinstance(G, nx.DiGraph):
        if is_ring_graph_gerichtet(G):
            return 'Ring Graph'
        elif is_stern_graph_gerichtet(G):
            return 'Stern Graph'
        return 'kein Stern- Baum- oder Ringgraph gefunden'
    elif isinstance(G, nx.Graph):
        if nx.is_tree(G):
            return 'Baum-Graph'
        elif is_ring_graph_ungerichtet(G):
            return 'Ring-Graph'
        elif is_stern_graph_ungerichtet(G):
            return 'Stern-Graph'
        else:
            return 'kein Stern- Baum- oder Ringgraph gefunden'
    #Überprüfen ob es ein Baum
    
#Graph erstellen
def graphErstellen(gewicht, richtung, nodes, edges):
    # Speichern des Graphen als PNG
    image_path = os.path.join(IMAGE_PATH, 'graph.png')
    
    matplotlib.use('Agg')  # Verwende ein nicht-interaktives Backend

    
    # Lösche das vorhandene Bild, falls es existiert
    if os.path.exists(image_path):
        os.remove(image_path)
        
    #Graph erstellen
    if richtung == 'ungerichtet':
        G = nx.Graph()
    elif richtung == 'gerichtet':
        G = nx.DiGraph()
    
    if gewicht == 'ungewichtet' and richtung == 'ungerichtet':
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        pos = nx.spring_layout(G)  # Layout für die Positionierung der Knoten
        nx.draw_networkx(G, pos, node_size=1000, node_color="lightblue", font_size=8)
        
    elif gewicht == 'ungewichtet'  and richtung == 'gerichtet':
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        pos = nx.spring_layout(G)  # Layout für die Positionierung der Knoten
        nx.draw_networkx(G, pos, node_size=1000, node_color="lightblue", font_size=8)
        
    elif gewicht == 'gewichtet'  and richtung == 'ungerichtet':
        G.add_nodes_from(nodes)
        G.add_weighted_edges_from(edges)
        pos = nx.spring_layout(G)  # Layout für die Positionierung der Knoten
        nx.draw_networkx(G, pos, node_size=1000, node_color="lightblue", font_size=8)
        edge_labels = nx.get_edge_attributes(G, 'weight')  # Erhalte die Gewichte als Dictionary
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
        
    elif gewicht == 'gewichtet'  and richtung == 'gerichtet':
        G.add_nodes_from(nodes)
        G.add_weighted_edges_from(edges)
        pos = nx.spring_layout(G)  # Layout für die Positionierung der Knoten
        nx.draw_networkx(G, pos, node_size=1000, node_color="lightblue", font_size=8)
        edge_labels = nx.get_edge_attributes(G, 'weight')  # Erhalte die Gewichte als Dictionary
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    #Überprüfen ob der Graph gerichet oder ungerichtet ist
    if isinstance(G, nx.DiGraph):
        if is_complete_graph_gerichtet(G):
            graph_state.vollständigkeit = "Der Graph ist vollständig."
        else:
            graph_state.vollständigkeit = "Der Graph ist nicht vollständig."
        #Eulerkreis überprüfen (Jede Kante wird einmal durchlaufen)
        if nx.is_eulerian(G):
            graph_state.eulerkreis = "Der Graph hat einen Eulerkreis."
        else:
            graph_state.eulerkreis = "Der Graph hat keinen Eulerkreis."
            
        #Hamiltonkreis überprüfen
        if find_hamiltonian_cycle_gerichtet(G):
            graph_state.hamiltonkreis = "Hamiltonkreis gefunden:", find_hamiltonian_cycle_ungerichtet(G)
        else:
            graph_state.hamiltonkreis = "Kein Hamiltonkreis gefunden."
    else:
    # Vollständigkeit des Graphen überprüfen (JEDER Knoten ist miteinander verbunden)
        if is_complete_graph_ungerichtet(G):
            graph_state.vollständigkeit = "Der Graph ist vollständig."
        else:
            graph_state.vollständigkeit = "Der Graph ist nicht vollständig."
            
        #Eulerkreis überprüfen (Jede Kante wird einmal durchlaufen)
        if nx.is_eulerian(G):
            graph_state.eulerkreis = "Der Graph hat einen Eulerkreis."
        else:
            graph_state.eulerkreis = "Der Graph hat keinen Eulerkreis."
            
        #Hamiltonkreis überprüfen
        if find_hamiltonian_cycle_ungerichtet(G):
            graph_state.hamiltonkreis = "Hamiltonkreis gefunden:", find_hamiltonian_cycle_ungerichtet(G)
        else:
            graph_state.hamiltonkreis = "Kein Hamiltonkreis gefunden."
    
    #Überorüft ob Stern, Baum ode Ring Graph da ist
    graph_state.art = art_des_Graphen_finden(G)
    
      
    plt.savefig(image_path)
    plt.close()  # Schließe das Bild
    
    return image_path  # Rückgabe des Bildpfad
    
    
# Stelle sicher, dass der Server hier gestartet wird
if __name__ == '__main__':
    app.run(debug=True)  # Server starten