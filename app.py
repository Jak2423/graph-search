from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import json
import folium
from folium import plugins
import os
from read_osm import RoadNetworkGraph

app = Flask(__name__)
CORS(app)  # Cross-Origin Resource Sharing идэвхжүүлэх

# Глобал хувьсагч - замын сүлжээ
road_network = None

def initialize_network():
    """Замын сүлжээг эхлүүлэх"""
    global road_network
    if road_network is None:
        try:
            print("Замын сүлжээг ачаалж байна...")
            road_network = RoadNetworkGraph("gis_osm_roads_free_1.shp")
            print("Амжилттай ачаалагдлаа!")
        except Exception as e:
            print(f"Алдаа: {e}")
            raise Exception(f"Shapefile уншихад алдаа: {str(e)}")

@app.route('/')
def index():
    """Үндсэн хуудас"""
    return render_template('index.html')

@app.route('/api/info', methods=['GET'])
def get_graph_info():
    """Графын ерөнхий мэдээлэл авах"""
    try:
        initialize_network()
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Shapefile ачаалахад алдаа: {str(e)}. Бүх файлууд байгаа эсэхийг шалгана уу (.shp, .shx, .dbf)'
        }), 500
    G = road_network.get_graph()

    return jsonify({
        'nodes': G.number_of_nodes(),
        'edges': G.number_of_edges(),
        'status': 'success'
    })

@app.route('/api/search', methods=['POST'])
def search_path():
    """
    Зам хайх API endpoint

    Request body:
    {
        "algorithm": "bfs" | "dfs" | "dijkstra",
        "start_lat": float,
        "start_lon": float,
        "end_lat": float,
        "end_lon": float
    }
    """
    try:
        initialize_network()
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Shapefile ачаалахад алдаа: {str(e)}. Бүх файлууд байгаа эсэхийг шалгана уу (.shp, .shx, .dbf)'
        }), 500

    data = request.json
    algorithm = data.get('algorithm', 'dijkstra')
    start_lat = float(data.get('start_lat'))
    start_lon = float(data.get('start_lon'))
    end_lat = float(data.get('end_lat'))
    end_lon = float(data.get('end_lon'))

    # Хамгийн ойр оройнуудыг олох
    start_node = road_network.find_nearest_node(start_lat, start_lon)
    end_node = road_network.find_nearest_node(end_lat, end_lon)

    if start_node is None or end_node is None:
        return jsonify({
            'status': 'error',
            'message': 'Орой олдсонгүй'
        }), 400

    # Алгоритм сонгох
    if algorithm == 'bfs':
        result = road_network.bfs(start_node, end_node)
    elif algorithm == 'dfs':
        result = road_network.dfs(start_node, end_node)
    elif algorithm == 'dijkstra':
        result = road_network.dijkstra(start_node, end_node)
    else:
        return jsonify({
            'status': 'error',
            'message': 'Буруу алгоритм'
        }), 400

    # Координатуудыг буцаах
    path_coords = [[node[1], node[0]] for node in result['path']]  # [lat, lon]
    visited_coords = [[node[1], node[0]] for node in result['visited'][:500]]  # Эхний 500

    return jsonify({
        'status': 'success',
        'algorithm': algorithm,
        'found': result['found'],
        'path': path_coords,
        'visited': visited_coords,
        'distance': round(result['distance'], 2),
        'path_length': len(result['path']),
        'visited_count': len(result['visited'])
    })

@app.route('/api/visualize', methods=['POST'])
def visualize_path():
    """
    Замыг газрын зураг дээр харуулах

    Request body: same as /api/search
    """
    try:
        initialize_network()
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Shapefile ачаалахад алдаа: {str(e)}. Бүх файлууд байгаа эсэхийг шалгана уу (.shp, .shx, .dbf)'
        }), 500

    data = request.json
    algorithm = data.get('algorithm', 'dijkstra')
    start_lat = float(data.get('start_lat'))
    start_lon = float(data.get('start_lon'))
    end_lat = float(data.get('end_lat'))
    end_lon = float(data.get('end_lon'))

    # Хамгийн ойр оройнуудыг олох
    start_node = road_network.find_nearest_node(start_lat, start_lon)
    end_node = road_network.find_nearest_node(end_lat, end_lon)

    if start_node is None or end_node is None:
        return jsonify({
            'status': 'error',
            'message': 'Орой олдсонгүй'
        }), 400

    # Алгоритм ажиллуулах
    if algorithm == 'bfs':
        result = road_network.bfs(start_node, end_node)
    elif algorithm == 'dfs':
        result = road_network.dfs(start_node, end_node)
    else:
        result = road_network.dijkstra(start_node, end_node)

    if not result['found']:
        return jsonify({
            'status': 'error',
            'message': 'Зам олдсонгүй'
        }), 404

    # Folium газрын зураг үүсгэх
    center_lat = (start_lat + end_lat) / 2
    center_lon = (start_lon + end_lon) / 2
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13)

    # Хайсан оройнуудыг харуулах (бүдэг цэгүүд)
    visited_coords = [[node[1], node[0]] for node in result['visited'][:500]]
    if visited_coords:
        for coord in visited_coords:
            folium.CircleMarker(
                location=coord,
                radius=2,
                color='orange',
                fill=True,
                fillOpacity=0.3,
                popup='Хайсан'
            ).add_to(m)

    # Олдсон замыг харуулах (улаан шугам)
    path_coords = [[node[1], node[0]] for node in result['path']]
    if path_coords:
        folium.PolyLine(
            path_coords,
            color='red',
            weight=5,
            opacity=0.8,
            popup=f"{algorithm.upper()} - {result['distance']:.2f} км"
        ).add_to(m)

    # Эхлэх болон төгсгөх цэгүүд
    folium.Marker(
        location=[start_lat, start_lon],
        popup='Эхлэх',
        icon=folium.Icon(color='green', icon='play')
    ).add_to(m)

    folium.Marker(
        location=[end_lat, end_lon],
        popup='Төгсгөх',
        icon=folium.Icon(color='red', icon='stop')
    ).add_to(m)

    # HTML файл үүсгэх
    map_filename = f'map_{algorithm}.html'
    map_path = os.path.join('static', map_filename)
    os.makedirs('static', exist_ok=True)
    m.save(map_path)

    return jsonify({
        'status': 'success',
        'map_url': f'/static/{map_filename}',
        'distance': round(result['distance'], 2),
        'path_length': len(result['path'])
    })

@app.route('/api/compare', methods=['POST'])
def compare_algorithms():
    """3 алгоритмыг харьцуулах"""
    try:
        initialize_network()
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Shapefile ачаалахад алдаа: {str(e)}. Бүх файлууд байгаа эсэхийг шалгана уу (.shp, .shx, .dbf)'
        }), 500

    data = request.json
    start_lat = float(data.get('start_lat'))
    start_lon = float(data.get('start_lon'))
    end_lat = float(data.get('end_lat'))
    end_lon = float(data.get('end_lon'))

    # Хамгийн ойр оройнуудыг олох
    start_node = road_network.find_nearest_node(start_lat, start_lon)
    end_node = road_network.find_nearest_node(end_lat, end_lon)

    if start_node is None or end_node is None:
        return jsonify({
            'status': 'error',
            'message': 'Орой олдсонгүй'
        }), 400

    # 3 алгоритм ажиллуулах
    import time

    results = {}

    # BFS
    start_time = time.time()
    bfs_result = road_network.bfs(start_node, end_node)
    bfs_time = (time.time() - start_time) * 1000  # миллисекунд

    results['bfs'] = {
        'found': bfs_result['found'],
        'distance': round(bfs_result['distance'], 2),
        'path_length': len(bfs_result['path']),
        'visited_count': len(bfs_result['visited']),
        'execution_time_ms': round(bfs_time, 2)
    }

    # DFS
    start_time = time.time()
    dfs_result = road_network.dfs(start_node, end_node)
    dfs_time = (time.time() - start_time) * 1000

    results['dfs'] = {
        'found': dfs_result['found'],
        'distance': round(dfs_result['distance'], 2),
        'path_length': len(dfs_result['path']),
        'visited_count': len(dfs_result['visited']),
        'execution_time_ms': round(dfs_time, 2)
    }

    # Dijkstra
    start_time = time.time()
    dijkstra_result = road_network.dijkstra(start_node, end_node)
    dijkstra_time = (time.time() - start_time) * 1000

    results['dijkstra'] = {
        'found': dijkstra_result['found'],
        'distance': round(dijkstra_result['distance'], 2),
        'path_length': len(dijkstra_result['path']),
        'visited_count': len(dijkstra_result['visited']),
        'execution_time_ms': round(dijkstra_time, 2)
    }

    return jsonify({
        'status': 'success',
        'results': results
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)

