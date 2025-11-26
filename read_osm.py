import geopandas as gpd
import networkx as nx
from shapely.geometry import Point
import numpy as np

class RoadNetworkGraph:
    """OpenStreetMap замын сүлжээг граф болгон хувирган ажиллах класс"""

    def __init__(self, shapefile_path):
        """
        OSM shapefile-г унших

        Args:
            shapefile_path: gis_osm_roads_free_1.shp файлын зам
        """
        self.gdf = gpd.read_file(shapefile_path)
        self.graph = nx.DiGraph()  # Чиглэлтэй граф
        self._build_graph()

    def _build_graph(self):
        """Shapefile-с граф үүсгэх"""
        print(f"Нийт {len(self.gdf)} замыг уншиж байна...")

        for idx, row in self.gdf.iterrows():
            if row.geometry is None:
                continue

            # LineString-н эхлэх ба төгсгөлийн цэгүүд
            coords = list(row.geometry.coords)

            for i in range(len(coords) - 1):
                start_node = coords[i]
                end_node = coords[i + 1]

                # Замын урт тооцох (км-ээр)
                distance = self._calculate_distance(start_node, end_node)

                # Хурд (км/цаг)
                max_speed = row.get('maxspeed', 50)
                if isinstance(max_speed, str):
                    try:
                        max_speed = float(max_speed.split()[0])
                    except:
                        max_speed = 50

                # Цаг тооцох (минут)
                time = (distance / max_speed) * 60 if max_speed > 0 else float('inf')

                # Граф руу ирмэг нэмэх
                self.graph.add_edge(
                    start_node,
                    end_node,
                    weight=distance,
                    time=time,
                    road_type=row.get('fclass', 'unknown'),
                    name=row.get('name', 'Unnamed'),
                    oneway=row.get('oneway', 'no')
                )

                # Хоёр чиглэлтэй зам бол буцаах ирмэг нэмэх
                if row.get('oneway', 'no') != 'yes':
                    self.graph.add_edge(
                        end_node,
                        start_node,
                        weight=distance,
                        time=time,
                        road_type=row.get('fclass', 'unknown'),
                        name=row.get('name', 'Unnamed'),
                        oneway='no'
                    )

        print(f"Граф үүслээ: {self.graph.number_of_nodes()} оройтой, "
              f"{self.graph.number_of_edges()} ирмэгтэй")

    def _calculate_distance(self, coord1, coord2):
        """
        Хоёр цэгийн хоорондох зайг Haversine томъёогоор тооцох

        Returns:
            Зай (км)
        """
        lat1, lon1 = coord1[1], coord1[0]
        lat2, lon2 = coord2[1], coord2[0]

        # Дэлхийн радиус (км)
        R = 6371.0

        lat1_rad = np.radians(lat1)
        lat2_rad = np.radians(lat2)
        delta_lat = np.radians(lat2 - lat1)
        delta_lon = np.radians(lon2 - lon1)

        a = np.sin(delta_lat/2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(delta_lon/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))

        return R * c

    def find_nearest_node(self, lat, lon):
        """
        Өгөгдсөн координатад хамгийн ойр оройг олох

        Args:
            lat: Өргөрөг
            lon: Уртраг

        Returns:
            Хамгийн ойр орой
        """
        target = (lon, lat)
        min_dist = float('inf')
        nearest = None

        for node in self.graph.nodes():
            dist = np.sqrt((node[0] - target[0])**2 + (node[1] - target[1])**2)
            if dist < min_dist:
                min_dist = dist
                nearest = node

        return nearest

    def get_graph(self):
        """Граф буцаах"""
        return self.graph

    def bfs(self, start_node, end_node):
        """
        Breadth-First Search (Өргөнөөр эхлэн хайх) алгоритм

        Args:
            start_node: Эхлэх орой
            end_node: Төгсгөх орой

        Returns:
            dict: {
                'path': Олдсон зам (жагсаалт),
                'visited': Хайсан оройнууд,
                'distance': Нийт зай,
                'found': Зам олдсон эсэх
            }
        """
        if start_node not in self.graph or end_node not in self.graph:
            return {'path': [], 'visited': [], 'distance': 0, 'found': False}

        from collections import deque

        queue = deque([(start_node, [start_node])])
        visited = set()
        visited_order = []

        while queue:
            current_node, path = queue.popleft()

            if current_node in visited:
                continue

            visited.add(current_node)
            visited_order.append(current_node)

            if current_node == end_node:
                # Замын нийт зайг тооцох
                total_distance = 0
                for i in range(len(path) - 1):
                    edge_data = self.graph.get_edge_data(path[i], path[i+1])
                    total_distance += edge_data.get('weight', 0)

                return {
                    'path': path,
                    'visited': visited_order,
                    'distance': total_distance,
                    'found': True
                }

            # Хөрш оройнуудыг дараалалд нэмэх
            for neighbor in self.graph.neighbors(current_node):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

        return {'path': [], 'visited': visited_order, 'distance': 0, 'found': False}

    def dfs(self, start_node, end_node):
        """
        Depth-First Search (Гүнээр эхлэн хайх) алгоритм

        Args:
            start_node: Эхлэх орой
            end_node: Төгсгөх орой

        Returns:
            dict: {
                'path': Олдсон зам (жагсаалт),
                'visited': Хайсан оройнууд,
                'distance': Нийт зай,
                'found': Зам олдсон эсэх
            }
        """
        if start_node not in self.graph or end_node not in self.graph:
            return {'path': [], 'visited': [], 'distance': 0, 'found': False}

        stack = [(start_node, [start_node])]
        visited = set()
        visited_order = []

        while stack:
            current_node, path = stack.pop()

            if current_node in visited:
                continue

            visited.add(current_node)
            visited_order.append(current_node)

            if current_node == end_node:
                # Замын нийт зайг тооцох
                total_distance = 0
                for i in range(len(path) - 1):
                    edge_data = self.graph.get_edge_data(path[i], path[i+1])
                    total_distance += edge_data.get('weight', 0)

                return {
                    'path': path,
                    'visited': visited_order,
                    'distance': total_distance,
                    'found': True
                }

            # Хөрш оройнуудыг стэк рүү нэмэх (эсрэг дарааллаар)
            neighbors = list(self.graph.neighbors(current_node))
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

        return {'path': [], 'visited': visited_order, 'distance': 0, 'found': False}

    def dijkstra(self, start_node, end_node):
        """
        Dijkstra алгоритм - хамгийн богино замыг олох

        Args:
            start_node: Эхлэх орой
            end_node: Төгсгөх орой

        Returns:
            dict: {
                'path': Хамгийн богино зам (жагсаалт),
                'visited': Хайсан оройнууд,
                'distance': Нийт зай,
                'found': Зам олдсон эсэх
            }
        """
        if start_node not in self.graph or end_node not in self.graph:
            return {'path': [], 'visited': [], 'distance': 0, 'found': False}

        import heapq

        # Priority queue: (зай, орой, зам)
        pq = [(0, start_node, [start_node])]
        distances = {start_node: 0}
        visited = set()
        visited_order = []

        while pq:
            current_dist, current_node, path = heapq.heappop(pq)

            if current_node in visited:
                continue

            visited.add(current_node)
            visited_order.append(current_node)

            if current_node == end_node:
                return {
                    'path': path,
                    'visited': visited_order,
                    'distance': current_dist,
                    'found': True
                }

            # Хөрш оройнуудыг шалгах
            for neighbor in self.graph.neighbors(current_node):
                if neighbor not in visited:
                    edge_data = self.graph.get_edge_data(current_node, neighbor)
                    new_dist = current_dist + edge_data.get('weight', 0)

                    if neighbor not in distances or new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        heapq.heappush(pq, (new_dist, neighbor, path + [neighbor]))

        return {'path': [], 'visited': visited_order, 'distance': 0, 'found': False}


# Жишээ ашиглалт
if __name__ == "__main__":
    # Shapefile унших
    road_network = RoadNetworkGraph("gis_osm_roads_free_1.shp")
    G = road_network.get_graph()

    print(f"\nГрафын мэдээлэл:")
    print(f"  - Оройн тоо: {G.number_of_nodes()}")
    print(f"  - Ирмэгийн тоо: {G.number_of_edges()}")

    # Жишээ: Алгоритмуудыг турших
    if G.number_of_nodes() > 0:
        nodes_list = list(G.nodes())[:100]  # Эхний 100 оройг авах
        if len(nodes_list) >= 2:
            start = nodes_list[0]
            end = nodes_list[min(50, len(nodes_list)-1)]

            print(f"\n{'='*60}")
            print(f"Эхлэх цэг: {start}")
            print(f"Төгсгөх цэг: {end}")
            print(f"{'='*60}")

            # BFS
            print("\n🔵 BFS (Өргөнөөр хайх):")
            bfs_result = road_network.bfs(start, end)
            print(f"  Зам олдсон: {bfs_result['found']}")
            if bfs_result['found']:
                print(f"  Замын урт: {len(bfs_result['path'])} орой")
                print(f"  Нийт зай: {bfs_result['distance']:.2f} км")
                print(f"  Хайсан орой: {len(bfs_result['visited'])}")

            # DFS
            print("\n🟢 DFS (Гүнээр хайх):")
            dfs_result = road_network.dfs(start, end)
            print(f"  Зам олдсон: {dfs_result['found']}")
            if dfs_result['found']:
                print(f"  Замын урт: {len(dfs_result['path'])} орой")
                print(f"  Нийт зай: {dfs_result['distance']:.2f} км")
                print(f"  Хайсан орой: {len(dfs_result['visited'])}")

            # Dijkstra
            print("\n🔴 Dijkstra (Хамгийн богино зам):")
            dijkstra_result = road_network.dijkstra(start, end)
            print(f"  Зам олдсон: {dijkstra_result['found']}")
            if dijkstra_result['found']:
                print(f"  Замын урт: {len(dijkstra_result['path'])} орой")
                print(f"  Нийт зай: {dijkstra_result['distance']:.2f} км")
                print(f"  Хайсан орой: {len(dijkstra_result['visited'])}")

            print(f"\n{'='*60}")