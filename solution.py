from collections import defaultdict
from heapq import heappop, heappush

# Read number of nodes and number of edges
n, m = map(int, input().split())

# Read edges
edges = defaultdict(list)
for _ in range(m):
    u, v, w = map(int, input().split())
    edges[u].append((v, w))
    edges[v].append((u, w))

# Read start and end nodes
x, y = map(int, input().split())

# Initialize globals
processed = [False] * (n + 1)
tin = defaultdict(lambda: -1)
low = defaultdict(lambda: -1)
timer = 0
bridges = []


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
        else:
            low[src] = min(low[src], tin[dest])


def dijkstra(start, end):
    if not edges[start]:
        return 0

    oo = float('inf')
    distances = defaultdict(lambda: oo)
    processed = [False] * (n + 1)
    distances[start] = 0
    h = [(distances[start], start)]

    while h:
        w_current, u = heappop(h)

        if processed[u]:
            continue

        processed[u] = True
        for v, w_next in edges[u]:
            if distances[v] > w_current + w_next:
                distances[v] = w_current + w_next
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
