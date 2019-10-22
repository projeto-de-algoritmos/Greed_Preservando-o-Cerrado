from collections import defaultdict
from collections import deque
from heapq import heappop, heappush
from mygraph import MyGraph

# Make graph
def make_graph(n):
    graph = MyGraph(graph_type='graph', size='20, 11, 25!', ratio='fill', fontsize=40)

    for v in range(1, n+1):
        graph.add_nodes(v)

    return graph

# Make graph img
def make_graph_img(graph, graph_name):
    graph.save_img('sistema_'+graph_name)

    print(f"O sistema {graph_name} foi salvo em {'sistema_'+graph_name}.png!")

# Read number of nodes and number of edges
n, m = map(int, input().split())

graph_original = make_graph(n)

# Read edges
edges = defaultdict(list)
for _ in range(m):
    u, v, w = map(int, input().split())
    edges[u].append((v, w))
    edges[v].append((u, w))
    graph_original.link(u, v, str(w))

# Read start and end nodes
x, y = map(int, input().split())

graph_original.change_color_node(x, "green")
graph_original.change_color_node(y, "red")

graph_reinforced = graph_original

make_graph_img(graph_original, "inicial")

# Initialize globals
processed = [False] * (n + 1)
tin = defaultdict(lambda: -1)
low = defaultdict(lambda: -1)
timer = 0
bridges = []
bridges_simples = {}

# From Tarjan
def fill_bridges(src, p=-1):
    global timer

    processed[src] = True
    timer += 1
    tin[src] = low[src] = timer

    for dest, _ in edges[src]:
        if dest == p:
            continue

        if not processed[dest]:
            fill_bridges(dest, src)
            low[src] = min(low[src], low[dest])

            if low[dest] > tin[src]:
                bridges.append((src, dest))
                bridges.append((dest, src))
                for e in edges[src]:
                    if e[0] == dest:
                        bridges_simples[src] = dest, e[1]
        else:
            low[src] = min(low[src], tin[dest])

pred = [-1 for _ in range(n+1)]

def dijkstra(start, end):
    global pred

    if not edges[start]:
        return 0

    oo = float('inf')
    distances = defaultdict(lambda: oo)
    processed = [False] * (n + 1)
    distances[start] = 0
    pred[start] = start
    h = [(distances[start], start)]

    while h:
        w_current, u = heappop(h)

        if processed[u]:
            continue

        processed[u] = True
        for v, w_next in edges[u]:
            if distances[v] > w_current + w_next:
                distances[v] = w_current + w_next
                pred[v] = u
                heappush(h, (distances[v], v))
    

    return distances[end]


if __name__ == '__main__':
    # Find bridges
    for u, is_processed in enumerate(processed):
        if not is_processed and u != 0:
            fill_bridges(u)

    # Double weight of bridges
    for u, v in bridges:
        for i, (dest, w) in enumerate(edges[u]):
            if dest == v:
                edges[u][i] = v, 2*w

    
    print(dijkstra(x, y))
    

    path = deque()

    aux_idx = y
    while aux_idx != x:
        path.appendleft(aux_idx)
        aux_idx = pred[aux_idx]

    path.appendleft(x)
    
    for i, n in enumerate(path):
        if i != len(path)-1:
            graph_reinforced.change_color_edge(n, path[i+1], "green")
    for k, v in bridges_simples.items():
        graph_reinforced.link(k, v[0], v[1], "brown")

    make_graph_img(graph_reinforced, "reforcado")
