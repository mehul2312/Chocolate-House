# Chocolate House Management System

It is a  Flask-based simple Python Application for a fictional chocolate house that uses SQLite to manage,
 - Seasonal flavor offerings 
 - Ingredient inventory
 - Customer flavor suggestions and allergy concerns

## Installation and Setup

### Local Setup

1. Clone the repository:

   git clone https://github.com/mehul2312/Chocolate-House.git


2. Create a virtual environment and activate it:

   python -m venv env

   source venv/bin/activate  , On Windows: venv\Scripts\activate


3. Install dependencies:

    pip install -r requirements.txt


4. Run the application:

    python app.py


### Docker Setup

1. Build the Docker image:

   docker build -t  l7informatics-task .


2. Run the container:

   docker run -p 5000:5000 l7informatics-task


## API Endpoints

### Flavors

- GET `/flavors` - List all flavors
- POST `/flavors` - Add a new flavor

```json
{
    "name": "Dark Chocolate Truffle",
    "season": "All-Season",
    "available": true
}
```

### Ingredients

- GET `/ingredients` - List all ingredients
- POST `/ingredients` - Add a new ingredient
- PUT `/ingredients/<id>` - Update ingredient quantity

```json
{
    "name": "Cocoa Powder",
    "quantity": 100.0,
    "unit": "kg",
    "allergen": false
}
```

### Customer Suggestions

- GET `/suggestions` - List all customer suggestions
- POST `/suggestions` - Add a new suggestion

```json
{
    "flavor_name": "Maple Walnut",
   
    "allergies": "Contains nuts"
}
```

## Manual Testing Steps

After running the command - python app.py , go to the browser(chrome) and open the localhost server "http://localhost:5000/" and do all flavour addition, inventory operations and  enter suggestions. 
(P.S.- Please refresh if needed)

alternativey on the terminal of vs code,follow the steps to get the output.

Test Flavor Management:

# List flavors
curl http://localhost:5000/flavors

# Add new flavor
curl -X POST http://localhost:5000/flavors \
     -H "Content-Type: application/json" \
     -d '{"name": "Berry Blast", "season": "Summer"}'

# For powershell - use-

Invoke-RestMethod -Uri "http://localhost:5000/flavors" `
    -Method Post `
    -Headers @{"Content-Type" = "application/json"} `
    -Body '{"name": "Berry Blast", "season": "Summer"}'



## Test Ingredient Management:

# List ingredients
curl http://localhost:5000/ingredients

# Add new ingredient
curl -X POST http://localhost:5000/ingredients \
     -H "Content-Type: application/json" \
     -d '{"name": "Sugar", "quantity": 50.0, "unit": "kg", "allergen": false}'

# Update ingredient quantity
curl -X PUT http://localhost:5000/ingredients/1 \
     -H "Content-Type: application/json" \
     -d '{"quantity": 75.0}'


# For powershell, use the command in following manner instead of curl:


Invoke-RestMethod -Uri "http://localhost:5000/ingredients" `
    -Method Post `
    -Headers @{"Content-Type" = "application/json"} `
    -Body '{"name": "Sugar", "quantity": 50.0, "unit": "kg", "allergen": false}'

## Test Customer Suggestions:

# List suggestions
curl http://localhost:5000/suggestions

# Add new suggestion
curl -X POST http://localhost:5000/suggestions \
     -H "Content-Type: application/json" \
     -d '{"flavor_name": "Lavender White" , "allergies": "None"}'

# For Powershell, use-
Invoke-RestMethod -Uri "http://localhost:5000/suggestions" `
    -Method Post `
    -Headers @{"Content-Type" = "application/json"} `
    -Body '{"flavor_name": "Lavender White", "allergies": "None"}'


 

## Code Structure

- `app.py`: Main application file with Flask routes and database operations
- `requirements.txt`: Python dependencies
- `Dockerfile`: Container configuration
- `templates`: it contains index.html for basic frontend. 
- Database is automatically initialized with sample data , which is given in the code.






