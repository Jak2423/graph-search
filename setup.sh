#!/bin/bash

# Граф хайлтын алгоритм - Суулгах скрипт

echo "=================================="
echo "Граф хайлтын алгоритм - Суулгалт"
echo "=================================="
echo ""

# Python шалгах
echo "1. Python хувилбар шалгаж байна..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 суулгаагүй байна!"
    echo "   https://www.python.org/downloads/ хаягаас татаж суулгана уу"
    exit 1
fi

echo "✅ Python суусан байна"
echo ""

# pip шалгах
echo "2. pip шалгаж байна..."
pip3 --version

if [ $? -ne 0 ]; then
    echo "❌ pip суулгаагүй байна!"
    exit 1
fi

echo "✅ pip суусан байна"
echo ""

# Virtual environment үүсгэх
echo "3. Virtual environment үүсгэж байна..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment үүссэн"
else
    echo "✅ Virtual environment аль хэдийн байна"
fi
echo ""

# Virtual environment идэвхжүүлэх
echo "4. Virtual environment идэвхжүүлж байна..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Virtual environment идэвхжүүлэхэд алдаа гарлаа!"
    exit 1
fi

echo "✅ Virtual environment идэвхжүүлсэн"
echo ""

# Сангууд суулгах
echo "5. Python сангуудыг суулгаж байна..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Сангууд суулгахад алдаа гарлаа!"
    exit 1
fi

echo "✅ Бүх сангууд амжилттай суусан"
echo ""

# Shapefile шалгах
echo "6. Өгөгдлийн файл шалгаж байна..."
if [ -f "gis_osm_roads_free_1.shp" ]; then
    echo "✅ gis_osm_roads_free_1.shp файл байна"
else
    echo "⚠️  gis_osm_roads_free_1.shp файл байхгүй байна!"
    echo "   https://download.geofabrik.de/ хаягаас татаж энэ хавтас руу хуулна уу"
fi
echo ""

echo "=================================="
echo "✅ СУУЛГАЛТ ДУУСЛАА!"
echo "=================================="
echo ""
echo "Дараах командуудыг ажиллуулж болно:"
echo ""
echo "  1. Тест ажиллуулах:"
echo "     source venv/bin/activate"
echo "     python3 test_algorithms.py"
echo ""
echo "  2. Веб сервер эхлүүлэх:"
echo "     source venv/bin/activate"
echo "     python3 app.py"
echo "     Дараа нь http://localhost:5000 руу ор"
echo ""

