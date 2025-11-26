#!/bin/bash

# Граф хайлтын алгоритм - Ажиллуулах скрипт

echo "=================================="
echo "Граф хайлтын алгоритм - Серверийг эхлүүлж байна"
echo "=================================="
echo ""

# Virtual environment идэвхжүүлэх
if [ -d "venv" ]; then
    echo "Virtual environment идэвхжүүлж байна..."
    source venv/bin/activate
    echo "✅ Идэвхжүүлсэн"
else
    echo "⚠️  Virtual environment байхгүй байна!"
    echo "   setup.sh скриптийг эхлээд ажиллуулна уу"
    echo "   ./setup.sh"
    exit 1
fi

echo ""

# Shapefile шалгах
if [ ! -f "gis_osm_roads_free_1.shp" ]; then
    echo "❌ gis_osm_roads_free_1.shp файл олдсонгүй!"
    echo "   Өгөгдлийн файл байх ёстой"
    exit 1
fi

echo "Flask серверийг эхлүүлж байна..."
echo "Хөтөч дээр http://localhost:5000 руу орно уу"
echo ""
echo "Зогсоох: Ctrl+C"
echo ""

python3 app.py

