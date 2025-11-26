"""
Алгоритмуудыг тестлэх скрипт
3 алгоритмыг ажиллуулж, үр дүнг харьцуулна
"""

from read_osm import RoadNetworkGraph
import time
import matplotlib.pyplot as plt

def test_algorithms():
    """Алгоритмуудыг тестлэх"""

    print("=" * 70)
    print("ГРАФ ХАЙЛТЫН АЛГОРИТМУУД - ТЕСТЛЭХ СКРИПТ")
    print("=" * 70)

    # Графыг ачаалах
    print("\n1️⃣ Графыг ачаалж байна...")
    start_time = time.time()
    road_network = RoadNetworkGraph("gis_osm_roads_free_1.shp")
    G = road_network.get_graph()
    load_time = time.time() - start_time

    print(f"   ✅ Амжилттай ачааллаа ({load_time:.2f} секунд)")
    print(f"   📊 Оройн тоо: {G.number_of_nodes():,}")
    print(f"   📊 Ирмэгийн тоо: {G.number_of_edges():,}")

    # Тест цэгүүдийг сонгох
    if G.number_of_nodes() == 0:
        print("\n❌ Граф хоосон байна!")
        return

    nodes_list = list(G.nodes())

    # Тест кейсүүд
    test_cases = [
        {
            'name': 'Тест 1: Ойрхон цэгүүд',
            'start_idx': 0,
            'end_idx': min(10, len(nodes_list)-1)
        },
        {
            'name': 'Тест 2: Дунд зай',
            'start_idx': 0,
            'end_idx': min(50, len(nodes_list)-1)
        },
        {
            'name': 'Тест 3: Хол цэгүүд',
            'start_idx': 0,
            'end_idx': min(100, len(nodes_list)-1)
        }
    ]

    all_results = []

    for test_idx, test_case in enumerate(test_cases, 1):
        print(f"\n{'=' * 70}")
        print(f"2️⃣ {test_case['name']}")
        print(f"{'=' * 70}")

        start_node = nodes_list[test_case['start_idx']]
        end_node = nodes_list[test_case['end_idx']]

        print(f"\n   Эхлэх орой: {start_node}")
        print(f"   Төгсгөх орой: {end_node}")

        results = {}

        # BFS
        print(f"\n   🔵 BFS ажиллуулж байна...")
        start_time = time.time()
        bfs_result = road_network.bfs(start_node, end_node)
        bfs_time = (time.time() - start_time) * 1000

        results['BFS'] = {
            'found': bfs_result['found'],
            'distance': bfs_result['distance'],
            'path_length': len(bfs_result['path']),
            'visited_count': len(bfs_result['visited']),
            'time_ms': bfs_time
        }

        if bfs_result['found']:
            print(f"      ✅ Зам олдсон")
            print(f"      📏 Зай: {bfs_result['distance']:.2f} км")
            print(f"      🔢 Замын урт: {len(bfs_result['path'])} орой")
            print(f"      👀 Хайсан: {len(bfs_result['visited'])} орой")
            print(f"      ⏱️  Хугацаа: {bfs_time:.2f} мс")
        else:
            print(f"      ❌ Зам олдсонгүй")

        # DFS
        print(f"\n   🟢 DFS ажиллуулж байна...")
        start_time = time.time()
        dfs_result = road_network.dfs(start_node, end_node)
        dfs_time = (time.time() - start_time) * 1000

        results['DFS'] = {
            'found': dfs_result['found'],
            'distance': dfs_result['distance'],
            'path_length': len(dfs_result['path']),
            'visited_count': len(dfs_result['visited']),
            'time_ms': dfs_time
        }

        if dfs_result['found']:
            print(f"      ✅ Зам олдсон")
            print(f"      📏 Зай: {dfs_result['distance']:.2f} км")
            print(f"      🔢 Замын урт: {len(dfs_result['path'])} орой")
            print(f"      👀 Хайсан: {len(dfs_result['visited'])} орой")
            print(f"      ⏱️  Хугацаа: {dfs_time:.2f} мс")
        else:
            print(f"      ❌ Зам олдсонгүй")

        # Dijkstra
        print(f"\n   🔴 Dijkstra ажиллуулж байна...")
        start_time = time.time()
        dijkstra_result = road_network.dijkstra(start_node, end_node)
        dijkstra_time = (time.time() - start_time) * 1000

        results['Dijkstra'] = {
            'found': dijkstra_result['found'],
            'distance': dijkstra_result['distance'],
            'path_length': len(dijkstra_result['path']),
            'visited_count': len(dijkstra_result['visited']),
            'time_ms': dijkstra_time
        }

        if dijkstra_result['found']:
            print(f"      ✅ Зам олдсон")
            print(f"      📏 Зай: {dijkstra_result['distance']:.2f} км (ХАМГИЙН БОГИНО)")
            print(f"      🔢 Замын урт: {len(dijkstra_result['path'])} орой")
            print(f"      👀 Хайсан: {len(dijkstra_result['visited'])} орой")
            print(f"      ⏱️  Хугацаа: {dijkstra_time:.2f} мс")
        else:
            print(f"      ❌ Зам олдсонгүй")

        all_results.append({
            'test_name': test_case['name'],
            'results': results
        })

    # Харьцуулалт
    print(f"\n{'=' * 70}")
    print("3️⃣ ХАРЬЦУУЛАЛТ")
    print(f"{'=' * 70}")

    for test_data in all_results:
        print(f"\n{test_data['test_name']}:")
        print(f"{'Алгоритм':<12} {'Зам':<8} {'Зай (км)':<12} {'Замын урт':<12} {'Хайсан':<10} {'Хугацаа (мс)':<15}")
        print("-" * 70)

        for algo_name, result in test_data['results'].items():
            found = "✅" if result['found'] else "❌"
            distance = f"{result['distance']:.2f}" if result['found'] else "N/A"
            path_len = str(result['path_length']) if result['found'] else "N/A"
            visited = str(result['visited_count'])
            time_val = f"{result['time_ms']:.2f}"

            print(f"{algo_name:<12} {found:<8} {distance:<12} {path_len:<12} {visited:<10} {time_val:<15}")

    # График зурах
    print(f"\n{'=' * 70}")
    print("4️⃣ График зурж байна...")
    print(f"{'=' * 70}")

    try:
        create_comparison_chart(all_results)
        print("   ✅ График амжилттай үүсгэгдлээ: comparison_chart.png")
    except Exception as e:
        print(f"   ⚠️ График үүсгэхэд алдаа: {e}")

    print(f"\n{'=' * 70}")
    print("✅ ТЕСТ ДУУСЛАА!")
    print(f"{'=' * 70}\n")

def create_comparison_chart(all_results):
    """Харьцуулалтын график зурах"""

    # Эхний тестийн үр дүнг авах
    if not all_results or not all_results[0]['results']:
        return

    results = all_results[0]['results']
    algorithms = list(results.keys())

    # Өгөгдөл бэлтгэх
    distances = [results[algo]['distance'] if results[algo]['found'] else 0 for algo in algorithms]
    times = [results[algo]['time_ms'] for algo in algorithms]
    visited = [results[algo]['visited_count'] for algo in algorithms]

    # 3 график үүсгэх
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

    colors = ['#3498db', '#2ecc71', '#e74c3c']

    # 1. Замын зай
    ax1.bar(algorithms, distances, color=colors)
    ax1.set_ylabel('Зай (км)', fontsize=12)
    ax1.set_title('Олдсон замын урт', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)

    # 2. Гүйцэтгэх хугацаа
    ax2.bar(algorithms, times, color=colors)
    ax2.set_ylabel('Хугацаа (мс)', fontsize=12)
    ax2.set_title('Гүйцэтгэх хугацаа', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)

    # 3. Хайсан орой
    ax3.bar(algorithms, visited, color=colors)
    ax3.set_ylabel('Хайсан оройн тоо', fontsize=12)
    ax3.set_title('Хайсан оройн тоо', fontsize=14, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig('comparison_chart.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    test_algorithms()

