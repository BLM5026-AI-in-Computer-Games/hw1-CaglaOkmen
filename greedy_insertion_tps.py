import networkx as nx
import matplotlib.pyplot as plt
import random
import math

random.seed(7)

# oklid mesafesi hesapla
def oklid( point1,  point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Graf olustur ve dondurur
def generate_graph(points, size):
    # Random Konum belirle
    for i in range(size):
        points[i] = (random.uniform(0, 50), random.uniform(0, 50))

    G = nx.Graph()
    # Node oluştur
    for index, point in points.items():
        G.add_node(index, pos=point)

    # Tüm nodelara Kenar ekle
    for i in range(len(points)):
        for y in range(i + 1, len(points)):
            wei = oklid(points[i], points[y])
            G.add_edge(i , y, weight=wei)
    return G

# Yolun Toplam uzunlugunu hesapla
def sum_distance(G, path):
    sum = 0
    for i in range(len(path) - 1):
        sum += G[path[i]][path[i + 1]]["weight"]
    return sum
    
# Ziyaret edilmemiş Nodlar arasından eklenmesi en ucuz Node u seçer ve yola ekleyerek dondurur.
def best_node_add(G, path, number):
    distance = None
    sm_dis = float('inf')
    for node_unvisited in G.nodes():
        if node_unvisited not in path:
            for i in range(len(path) - 1):
                    n1 = path[i]
                    n2 = path[i + 1]
                    distance = G[n1][node_unvisited]["weight"] + G[node_unvisited][n2]["weight"] - G[n1][n2]["weight"]
                    if distance < sm_dis:
                        sm_dis = distance
                        where = i + 1
                        add_node = node_unvisited
    number += 1              
    path.insert(where, add_node)
    G.nodes[add_node]['Labels'] = number
    return path

def tps_insertion(G):
    # Random 3 Node belirle
    nodes = list(G.nodes())
    path = random.sample(nodes, 3)
    # ilk secilen Node lara 0 labeli eklendi.
    for node in G.nodes():
        if node in path:
            G.nodes[node]['Labels'] = 0
    path.append(path[0])
    
    number = 0
    # Tum Nodelar ziyaret edilene kadar calistir. En iyi node veren yolu gunceller
    while len(path) - 1 < len(G.nodes()):
        path = best_node_add(G, path, number)
        number += 1

    #Toplam yolu hesapla
    sum = sum_distance(G, path)
    print(path)
    return sum, path

# Grafı ve Secilen yolu çiz
def draw_graph(G, points, path_edge, tps_sum):
    nx.draw(G, pos=points , with_labels=True, node_color='red', edge_color="grey",
            font_color="white", node_size=280, font_size=10, width=0.5)
    nx.draw_networkx_edges(G, pos=points, edgelist=path_edge, width=2) 
    label_points = {n: (x, y + 2) for n, (x, y) in points.items()}
    nx.draw_networkx_labels(G, pos=label_points, labels=nx.get_node_attributes(G, 'Labels'), 
                            font_size=10, font_color="blue", font_weight="bold")
    plt.text(0, 0, f"Toplam Gidilen Mesafe: {tps_sum}", fontsize=11)
    plt.xlim(-3, 55)
    plt.ylim(-3, 55)
    plt.show()

if __name__ == '__main__':
    points = {}
    path_edge = []
    G = generate_graph(points, 15) # 15 Node lu Graf uretir
    tps_sum, path = tps_insertion(G) 
    # izlenen yol Kenarları belirtilmesi için 
    path_edge = [(path[i], path[i+1]) for i in range(len(path)-1)] 
    print(f"Greedy Insertion Algoritması ile TPS sonucu: {tps_sum}")
    draw_graph(G, points, path_edge, tps_sum)