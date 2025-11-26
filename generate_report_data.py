"""
Тайланд шаардлагатай бүх график, хүснэгт, үр дүнг үүсгэх скрипт
"""

from read_osm import RoadNetworkGraph
import time
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import json

# Matplotlib-г монгол үсэг дэмжүүлэх
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

def run_comprehensive_tests():
    """Иж бүрэн тест ажиллуулж үр дүн үүсгэх"""

    print("=" * 80)
    print("ТАЙЛАНГИЙН ӨГӨГДӨЛ ҮҮСГЭХ")
    print("=" * 80)

    # Графыг ачаалах
    print("\n📊 Графыг ачаалж байна...")
    start_time = time.time()
    road_network = RoadNetworkGraph("gis_osm_roads_free_1.shp")
    G = road_network.get_graph()
    load_time = time.time() - start_time

    print(f"✅ Ачааллаа ({load_time:.2f} секунд)")
    print(f"   - Оройн тоо: {G.number_of_nodes():,}")
    print(f"   - Ирмэгийн тоо: {G.number_of_edges():,}")

    if G.number_of_nodes() == 0:
        print("\n❌ Граф хоосон байна!")
        return

    nodes_list = list(G.nodes())

    # Тест кейсүүд - өөр өөр зайнууд
    test_cases = [
        {
            'name': 'Ойрхон зай (10 орой)',
            'start_idx': 0,
            'end_idx': min(10, len(nodes_list)-1)
        },
      #   {
      #       'name': 'Дунд зай (50 орой)',
      #       'start_idx': 0,
      #       'end_idx': min(50, len(nodes_list)-1)
      #   },
      #   {
      #       'name': 'Холын зай (100 орой)',
      #       'start_idx': 0,
      #       'end_idx': min(100, len(nodes_list)-1)
      #   }
    ]

    all_results = []

    for test_idx, test_case in enumerate(test_cases, 1):
        print(f"\n{'=' * 80}")
        print(f"ТЕСТ {test_idx}: {test_case['name']}")
        print(f"{'=' * 80}")

        start_node = nodes_list[test_case['start_idx']]
        end_node = nodes_list[test_case['end_idx']]

        print(f"\nЭхлэх: {start_node}")
        print(f"Төгсгөх: {end_node}")

        results = {}

        # BFS
        print(f"\n🔵 BFS ажиллуулж байна...")
        start_time = time.time()
        bfs_result = road_network.bfs(start_node, end_node)
        bfs_time = (time.time() - start_time) * 1000

        results['BFS'] = {
            'found': bfs_result['found'],
            'distance': round(bfs_result['distance'], 2),
            'path_length': len(bfs_result['path']),
            'visited_count': len(bfs_result['visited']),
            'time_ms': round(bfs_time, 2)
        }

        print(f"   ✅ Дууслаа: {results['BFS']}")

        # DFS
        print(f"\n🟢 DFS ажиллуулж байна...")
        start_time = time.time()
        dfs_result = road_network.dfs(start_node, end_node)
        dfs_time = (time.time() - start_time) * 1000

        results['DFS'] = {
            'found': dfs_result['found'],
            'distance': round(dfs_result['distance'], 2),
            'path_length': len(dfs_result['path']),
            'visited_count': len(dfs_result['visited']),
            'time_ms': round(dfs_time, 2)
        }

        print(f"   ✅ Дууслаа: {results['DFS']}")

        # Dijkstra
        print(f"\n🔴 Dijkstra ажиллуулж байна...")
        start_time = time.time()
        dijkstra_result = road_network.dijkstra(start_node, end_node)
        dijkstra_time = (time.time() - start_time) * 1000

        results['Dijkstra'] = {
            'found': dijkstra_result['found'],
            'distance': round(dijkstra_result['distance'], 2),
            'path_length': len(dijkstra_result['path']),
            'visited_count': len(dijkstra_result['visited']),
            'time_ms': round(dijkstra_time, 2)
        }

        print(f"   ✅ Дууслаа: {results['Dijkstra']}")

        all_results.append({
            'test_name': test_case['name'],
            'test_number': test_idx,
            'results': results
        })

    # Үр дүнг JSON файлд хадгалах
    print(f"\n{'=' * 80}")
    print("📝 Үр дүнг хадгалж байна...")

    with open('test_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            'graph_info': {
                'nodes': G.number_of_nodes(),
                'edges': G.number_of_edges(),
                'load_time': round(load_time, 2)
            },
            'tests': all_results
        }, f, ensure_ascii=False, indent=2)

    print("✅ test_results.json файлд хадгалагдлаа")

    # Харьцуулалтын хүснэгт хэвлэх
    print(f"\n{'=' * 80}")
    print("📊 ХАРЬЦУУЛАЛТЫН ХҮСНЭГТ")
    print(f"{'=' * 80}")

    for test_data in all_results:
        print(f"\n{test_data['test_name']}:")
        print(f"{'Алгоритм':<12} {'Олдсон':<8} {'Зай (км)':<12} {'Замын урт':<12} {'Хайсан':<12} {'Хугацаа (мс)':<15}")
        print("-" * 80)

        for algo_name, result in test_data['results'].items():
            found = "✅" if result['found'] else "❌"
            distance = f"{result['distance']:.2f}" if result['found'] else "N/A"
            path_len = str(result['path_length']) if result['found'] else "N/A"
            visited = str(result['visited_count'])
            time_val = f"{result['time_ms']:.2f}"

            print(f"{algo_name:<12} {found:<8} {distance:<12} {path_len:<12} {visited:<12} {time_val:<15}")

    # Графикууд үүсгэх
    print(f"\n{'=' * 80}")
    print("📈 Графикууд үүсгэж байна...")
    print(f"{'=' * 80}")

    create_all_charts(all_results)

    print(f"\n{'=' * 80}")
    print("✅ БҮГД ДУУСЛАА!")
    print(f"{'=' * 80}")
    print("\nҮүссэн файлууд:")
    print("  - test_results.json")
    print("  - figure1_comparison_all.png")
    print("  - figure2_distance_comparison.png")
    print("  - figure3_time_comparison.png")
    print("  - figure4_visited_comparison.png")
    print("  - figure5_performance_summary.png")
    print("\nТайландаа эдгээр зургуудыг ашиглаарай!")

def create_all_charts(all_results):
    """Бүх график үүсгэх"""

    # Эхний тестийн үр дүн (дунд зай)
    test_data = all_results[1] if len(all_results) > 1 else all_results[0]
    results = test_data['results']

    algorithms = list(results.keys())
    colors = ['#3498db', '#2ecc71', '#e74c3c']

    # График 1: Бүх үзүүлэлтийг харьцуулах (3x2 grid)
    fig = plt.figure(figsize=(15, 10))
    fig.suptitle('Зураг 1: Граф хайлтын алгоритмуудын иж бүрэн харьцуулалт',
                 fontsize=16, fontweight='bold', y=0.995)

    # 1. Замын зай
    ax1 = plt.subplot(2, 3, 1)
    distances = [results[algo]['distance'] if results[algo]['found'] else 0 for algo in algorithms]
    bars1 = ax1.bar(algorithms, distances, color=colors, alpha=0.8, edgecolor='black')
    ax1.set_ylabel('Зай (км)', fontsize=11, fontweight='bold')
    ax1.set_title('(a) Олдсон замын урт', fontsize=12, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    for bar, val in zip(bars1, distances):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f} км', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # 2. Гүйцэтгэх хугацаа
    ax2 = plt.subplot(2, 3, 2)
    times = [results[algo]['time_ms'] for algo in algorithms]
    bars2 = ax2.bar(algorithms, times, color=colors, alpha=0.8, edgecolor='black')
    ax2.set_ylabel('Хугацаа (мс)', fontsize=11, fontweight='bold')
    ax2.set_title('(b) Гүйцэтгэх хугацаа', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    for bar, val in zip(bars2, times):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f} мс', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # 3. Хайсан орой
    ax3 = plt.subplot(2, 3, 3)
    visited = [results[algo]['visited_count'] for algo in algorithms]
    bars3 = ax3.bar(algorithms, visited, color=colors, alpha=0.8, edgecolor='black')
    ax3.set_ylabel('Хайсан оройн тоо', fontsize=11, fontweight='bold')
    ax3.set_title('(c) Хайлтын өргөн', fontsize=12, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3, linestyle='--')
    for bar, val in zip(bars3, visited):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{val}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # 4. Замын орой
    ax4 = plt.subplot(2, 3, 4)
    path_lengths = [results[algo]['path_length'] if results[algo]['found'] else 0 for algo in algorithms]
    bars4 = ax4.bar(algorithms, path_lengths, color=colors, alpha=0.8, edgecolor='black')
    ax4.set_ylabel('Замын урт (орой)', fontsize=11, fontweight='bold')
    ax4.set_title('(d) Олдсон замын орой тоо', fontsize=12, fontweight='bold')
    ax4.grid(axis='y', alpha=0.3, linestyle='--')
    for bar, val in zip(bars4, path_lengths):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{val}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # 5. Үр ашиг (зай/хугацаа)
    ax5 = plt.subplot(2, 3, 5)
    efficiency = [distances[i]/times[i]*1000 if times[i] > 0 else 0 for i in range(len(algorithms))]
    bars5 = ax5.bar(algorithms, efficiency, color=colors, alpha=0.8, edgecolor='black')
    ax5.set_ylabel('Үр ашиг (км/сек)', fontsize=11, fontweight='bold')
    ax5.set_title('(e) Үр ашиг', fontsize=12, fontweight='bold')
    ax5.grid(axis='y', alpha=0.3, linestyle='--')
    for bar, val in zip(bars5, efficiency):
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # 6. Тайлбар
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('off')
    legend_text = f"""
Тайлбар:
• BFS: Өргөнөөр хайх
• DFS: Гүнээр хайх
• Dijkstra: Хамгийн богино зам

Үр дүн:
• Хамгийн богино: {algorithms[distances.index(min([d for d in distances if d > 0]))]}
• Хамгийн хурдан: {algorithms[times.index(min(times))]}
• Хамгийн үр ашигтай: {algorithms[efficiency.index(max(efficiency))]}
"""
    ax6.text(0.1, 0.5, legend_text, fontsize=11, verticalalignment='center',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig('figure1_comparison_all.png', dpi=300, bbox_inches='tight')
    print("✅ figure1_comparison_all.png үүслээ")
    plt.close()

    # График 2: 3 тестийн зайг харьцуулах
    if len(all_results) >= 3:
        fig, ax = plt.figure(figsize=(12, 7)), plt.gca()

        x = np.arange(len(all_results))
        width = 0.25

        for i, algo in enumerate(algorithms):
            distances = [test['results'][algo]['distance'] if test['results'][algo]['found'] else 0
                        for test in all_results]
            ax.bar(x + i*width, distances, width, label=algo, color=colors[i],
                   alpha=0.8, edgecolor='black')

        ax.set_xlabel('Тестийн нөхцөл', fontsize=12, fontweight='bold')
        ax.set_ylabel('Зай (км)', fontsize=12, fontweight='bold')
        ax.set_title('Зураг 2: Өөр өөр зайн дахь алгоритмуудын гүйцэтгэл',
                     fontsize=14, fontweight='bold')
        ax.set_xticks(x + width)
        ax.set_xticklabels([test['test_name'] for test in all_results], fontsize=10)
        ax.legend(fontsize=11)
        ax.grid(axis='y', alpha=0.3, linestyle='--')

        plt.tight_layout()
        plt.savefig('figure2_distance_comparison.png', dpi=300, bbox_inches='tight')
        print("✅ figure2_distance_comparison.png үүслээ")
        plt.close()

    # График 3: Хугацааны харьцуулалт
    if len(all_results) >= 3:
        fig, ax = plt.figure(figsize=(12, 7)), plt.gca()

        for i, algo in enumerate(algorithms):
            times = [test['results'][algo]['time_ms'] for test in all_results]
            ax.plot(range(len(all_results)), times, marker='o', linewidth=2.5,
                   markersize=10, label=algo, color=colors[i])

        ax.set_xlabel('Тестийн нөхцөл', fontsize=12, fontweight='bold')
        ax.set_ylabel('Хугацаа (мс)', fontsize=12, fontweight='bold')
        ax.set_title('Зураг 3: Гүйцэтгэх хугацааны харьцуулалт',
                     fontsize=14, fontweight='bold')
        ax.set_xticks(range(len(all_results)))
        ax.set_xticklabels([test['test_name'] for test in all_results], fontsize=10)
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3, linestyle='--')

        plt.tight_layout()
        plt.savefig('figure3_time_comparison.png', dpi=300, bbox_inches='tight')
        print("✅ figure3_time_comparison.png үүслээ")
        plt.close()

    # График 4: Хайсан оройн харьцуулалт
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Зураг 4: Хайлтын өргөн ба гүнийг харьцуулах',
                 fontsize=14, fontweight='bold')

    # Pie chart - хайсан орой
    visited_data = [results[algo]['visited_count'] for algo in algorithms]
    ax1.pie(visited_data, labels=algorithms, colors=colors, autopct='%1.1f%%',
            startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax1.set_title('(a) Хайсан оройн хувь', fontsize=12, fontweight='bold')

    # Bar chart - замын орой vs хайсан орой
    x = np.arange(len(algorithms))
    width = 0.35

    path_data = [results[algo]['path_length'] if results[algo]['found'] else 0 for algo in algorithms]
    visited_data = [results[algo]['visited_count'] for algo in algorithms]

    ax2.bar(x - width/2, path_data, width, label='Замын орой', color='#3498db',
            alpha=0.8, edgecolor='black')
    ax2.bar(x + width/2, visited_data, width, label='Хайсан орой', color='#e74c3c',
            alpha=0.8, edgecolor='black')

    ax2.set_ylabel('Оройн тоо', fontsize=11, fontweight='bold')
    ax2.set_title('(b) Зам олох үр ашиг', fontsize=12, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(algorithms)
    ax2.legend(fontsize=10)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.savefig('figure4_visited_comparison.png', dpi=300, bbox_inches='tight')
    print("✅ figure4_visited_comparison.png үүслээ")
    plt.close()

    # График 5: Нэгтгэсэн үнэлгээ
    fig = plt.figure(figsize=(12, 8))
    fig.suptitle('Зураг 5: Алгоритмуудын нэгтгэсэн үнэлгээ',
                 fontsize=14, fontweight='bold')

    # Normalize metrics (0-1)
    def normalize(values):
        min_val, max_val = min(values), max(values)
        if max_val == min_val:
            return [1] * len(values)
        return [(v - min_val) / (max_val - min_val) for v in values]

    # Lower is better for these
    norm_distances = [1 - x for x in normalize(distances)]
    norm_times = [1 - x for x in normalize(times)]
    norm_visited = [1 - x for x in normalize(visited)]

    # Higher is better
    norm_path = normalize(path_lengths)

    categories = ['Замын\nбогино', 'Хугацаа\nхурдан', 'Хайсан\nцөөн', 'Зам\nтодорхой']

    for i, algo in enumerate(algorithms):
        values = [norm_distances[i], norm_times[i], norm_visited[i], norm_path[i]]
        values += values[:1]  # Close the plot

        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]

        ax = plt.subplot(1, 3, i+1, projection='polar')
        ax.plot(angles, values, 'o-', linewidth=2, color=colors[i], label=algo)
        ax.fill(angles, values, alpha=0.25, color=colors[i])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=10)
        ax.set_ylim(0, 1)
        ax.set_title(algo, fontsize=12, fontweight='bold', pad=20)
        ax.grid(True)

    plt.tight_layout()
    plt.savefig('figure5_performance_summary.png', dpi=300, bbox_inches='tight')
    print("✅ figure5_performance_summary.png үүслээ")
    plt.close()

if __name__ == "__main__":
    run_comprehensive_tests()

