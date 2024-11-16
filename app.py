# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
from datetime import datetime
import logging
from dataclasses import dataclass
from typing import List, Optional

# Data Classes for ts
@dataclass
class Flavor:
    id: Optional[int]
    name: str
    season: str
    available: bool

@dataclass
class Ingredient:
    id: Optional[int]
    name: str
    quantity: float
    unit: str
    allergen: bool

@dataclass
class CustomerSuggestion:
    id: Optional[int]
    flavor_name: str
    allergies: str
    submitted_date: str

app = Flask(__name__)
CORS(app)

# Database initialization
def init_db():
    with sqlite3.connect('chocolate_house.db') as conn:
        cursor = conn.cursor()
        
        # Creating tables with proper constraints
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS flavors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                season TEXT NOT NULL,
                available BOOLEAN DEFAULT TRUE,
                CHECK (season IN ('Spring', 'Summer', 'autumn', 'Winter', 'All-Season'))
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                quantity REAL NOT NULL CHECK (quantity >= 0),
                unit TEXT NOT NULL,
                allergen BOOLEAN NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customer_suggestions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flavor_name TEXT NOT NULL,
                allergies TEXT,
                submitted_date TEXT NOT NULL
            )
        ''')
        
        # Inserting few sample data to let the program fetch details
        try:
            cursor.execute('''
                INSERT INTO flavors (name, season)
                VALUES 
                    ('Dark Chocolate ', 'All-Season'),
                    ('Hazelnut Choclate', 'autumn'),
                    ('Apple Blend', 'Winter')
            ''')
            
            cursor.execute('''
                INSERT INTO ingredients (name, quantity, unit, allergen)
                VALUES 
                    ('Cocoa Powder', 100.0, 'kg', FALSE),
                    ('Milk Powder', 50.0, 'kg', TRUE),
                    ('walnuts', 25.0, 'kg', TRUE),
                    ('salt',1.0,'kg',FALSE)
            ''')
            
            conn.commit()
        except sqlite3.IntegrityError:
            # if sample data exists the pass
            pass

# Initialize database 
init_db()

@app.errorhandler(Exception)
def handle_error(error):
    logging.error(f"Error occurred: {str(error)}")
    return jsonify({"error": str(error)}), 500

@app.route('/')
def index():
    return render_template('index.html')

# Flavor Management Endpoints like get flavour and post flavour
@app.route('/flavors', methods=['GET'])
def get_flavors():
    with sqlite3.connect('chocolate_house.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM flavors')
        flavors = cursor.fetchall()
        return jsonify([{
            'id': f[0],
            'name': f[1],
            'season': f[2],
            'available': bool(f[3])
        } for f in flavors])

@app.route('/flavors', methods=['POST'])
def add_flavor():
    data = request.get_json()
    flavor = Flavor(
        id=None,
        name=data['name'],
        season=data['season'],
        available=data.get('available', True)
    )
    
    with sqlite3.connect('chocolate_house.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO flavors (name, season,available) VALUES (?, ?, ?)',
            (flavor.name, flavor.season, flavor.available)
        )
        return jsonify({"message": "Flavor added successfully"}), 201

# Ingredient management endpoints like get ingridents and post ingridients
@app.route('/ingredients', methods=['GET'])
def get_ingredients():
    with sqlite3.connect('chocolate_house.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ingredients')
        ingredients = cursor.fetchall()
        return jsonify([{
            'id': i[0],
            'name': i[1],
            'quantity': i[2],
            'unit': i[3],
            'allergen': bool(i[4])
        } for i in ingredients])

@app.route('/ingredients', methods=['POST'])
def add_ingredient():
    data = request.get_json()
    ingredient = Ingredient(
        id=None,
        name=data['name'],
        quantity=float(data['quantity']),
        unit=data['unit'],
        allergen=bool(data['allergen'])
    )
    
    with sqlite3.connect('chocolate_house.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO ingredients (name, quantity, unit, allergen) VALUES (?, ?, ?, ?)',
            (ingredient.name, ingredient.quantity, ingredient.unit, ingredient.allergen)
        )
        return jsonify({"message": "Ingredient added successfully"}), 201

@app.route('/ingredients/<int:id>', methods=['PUT'])
def update_ingredient(id):
    data = request.get_json()
    with sqlite3.connect('chocolate_house.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE ingredients SET quantity = ? WHERE id = ?',
            (float(data['quantity']), id)
        )
        if cursor.rowcount == 0:
            return jsonify({"error": "Ingredient not found"}), 404
        return jsonify({"message": "Ingredient updated successfully"})

# Customer suggestions endpoints to get and post suggestions
@app.route('/suggestions', methods=['POST'])
def add_suggestion():
    data = request.get_json()
    suggestion = CustomerSuggestion(
        id=None,
        flavor_name=data['flavor_name'],
        allergies=data.get('allergies', ''),
        submitted_date=datetime.now().isoformat()
    )
    
    with sqlite3.connect('chocolate_house.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO customer_suggestions (flavor_name, allergies, submitted_date) VALUES (?, ?, ?)',
            (suggestion.flavor_name, suggestion.allergies, suggestion.submitted_date)
        )
        return jsonify({"message": "Suggestion added successfully"}), 201

@app.route('/suggestions', methods=['GET'])
def get_suggestions():
    with sqlite3.connect('chocolate_house.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customer_suggestions')
        suggestions = cursor.fetchall()
        return jsonify([{
            'id': s[0],
            'flavor_name': s[1],
            'allergies': s[2],
            'submitted_date': s[3]
        } for s in suggestions])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

