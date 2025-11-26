# ⚠️ Shapefile Файлын Асуудал Засах

## Асуудал

Та зөвхөн `.shp` файлыг хуулсан байна. Shapefile нь **олон файлаас** бүрддэг!

## Шаардлагатай файлууд

Дараах **БҮХ** файлууд байх ёстой:

```
gis_osm_roads_free_1.shp   ✅ (танд байна)
gis_osm_roads_free_1.shx   ❌ (дутуу - index файл)
gis_osm_roads_free_1.dbf   ❌ (дутуу - attribute data)
gis_osm_roads_free_1.prj   ⚪ (optional - coordinate system)
gis_osm_roads_free_1.cpg   ⚪ (optional - encoding)
```

## Засах арга

### Арга 1: Бүх файлуудыг хуулах (Хамгийн энгийн)

1. **Эх файлуудыг олох:**

   -  Өөрийн татсан ZIP файлаас эсвэл folder-с
   -  Бүх `gis_osm_roads_free_1.*` файлуудыг хайх

2. **Бүх файлуудыг хуулах:**

   ```bash
   # Жишээ: Хэрэв Downloads-д татсан бол
   cp ~/Downloads/gis_osm_roads_free_1.* /Users/jak/Downloads/lab1/
   ```

3. **Шалгах:**
   ```bash
   cd /Users/jak/Downloads/lab1
   ls -la gis_osm_roads_free_1.*
   ```

### Арга 2: Дахин татах

1. **OpenStreetMap өгөгдөл татах:**

   -  https://download.geofabrik.de/ руу ор
   -  Өөрийн улс/хотоо сонго (жишээ: Asia → Mongolia)
   -  ZIP файл тат

2. **Задлах:**
   ```bash
   unzip -j [downloaded-file].zip "gis_osm_roads_free_1.*" -d /Users/jak/Downloads/lab1/
   ```

### Арга 3: Өөр өгөгдөл ашиглах (жижиг тест хийхэд)

Хэрэв том файл байвал, жижиг өгөгдөл дээр тест хийж болно:

```python
# test_small.py үүсгэх
import geopandas as gpd
from shapely.geometry import LineString
import pandas as pd

# Жижиг өгөгдөл үүсгэх
data = {
    'geometry': [
        LineString([(106.9177, 47.9186), (106.9277, 47.9286)]),
        LineString([(106.9277, 47.9286), (106.9377, 47.9386)]),
        LineString([(106.9177, 47.9186), (106.9077, 47.9086)]),
    ],
    'name': ['Road 1', 'Road 2', 'Road 3'],
    'fclass': ['primary', 'secondary', 'primary'],
    'maxspeed': [60, 40, 60],
    'oneway': ['no', 'no', 'no']
}

gdf = gpd.GeoDataFrame(data, crs='EPSG:4326')
gdf.to_file('gis_osm_roads_free_1.shp')
print("✅ Жижиг тест файл үүсгэгдлээ!")
```

Дараа нь:

```bash
python3 test_small.py
python3 app.py
```

## Серверийг дахин эхлүүлэх

Файлуудыг хуулсны дараа:

1. **Серверийг зогсоох:** Ctrl+C
2. **Дахин эхлүүлэх:**
   ```bash
   python3 app.py
   ```
3. **Хөтөч дээр:** http://localhost:3000

## Шалгах

Серверийг ажиллуулахад ийм мэдээлэл гарах ёстой:

```
Замын сүлжээг ачаалж байна...
Нийт 1234 замыг уншиж байна...
Граф үүслээ: 5678 оройтой, 9012 ирмэгтэй
Амжилттай ачаалагдлаа!
```

## Асуудал үргэлжилвэл

Хэрэв асуудал үргэлжилбэл, QGIS эсвэл онлайн хувиргагч ашиглан Shapefile-аа шалгаж болно:

-  https://mygeodata.cloud/converter/shp-to-geojson
-  Shapefile → GeoJSON хувиргаж, дараа нь кодоо GeoJSON уншуулах

---

**Тусламж хэрэгтэй бол:** README.md уншаарай!
