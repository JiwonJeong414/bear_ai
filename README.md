# Brand Mentions Analysis Project

This project consists of two stages:
1. **Stage 1**: Web scraping to collect brand mentions from ChatGPT responses
2. **Stage 2**: API to serve brand mention metrics

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bear_ai
   ```

2. **Set up environment variables**
   Create a `.env` file in the `api/` directory:
   ```bash
   # Database configuration
   DATABASE_URL='YOUR_DATABASE'
   
   # CSV file path from Stage 1 results
   CSV_FILE_PATH='YOUR_PATH'
   ```

3. **Install dependencies**
   ```bash
   # Install Stage 1 dependencies
   pip install -r requirements.txt
   
   # Install Stage 2 dependencies
   cd api
   pip install -r requirements.txt
   
   # Install Playwright
   playwright install
   ```

## Stage 1: Web Scraping

### Overview
Stage 1 automates the process of querying ChatGPT with sportswear-related prompts and extracting brand mentions for:
- Nike
- Adidas
- Hoka
- New Balance
- Jordan

### How to Run Stage 1

1. **Navigate to the project root**
   ```bash
   cd /path/to/bear_ai
   ```

2. **Run the scraping script**
   ```bash
   python async.py
   ```

3. **What happens during execution:**
   - Opens Firefox browser via Playwright
   - Navigates to ChatGPT through Proxyium
   - Sends 10 predefined prompts about sportswear
   - Extracts and counts brand mentions from responses
   - Saves results to `brand_analysis_results.csv`

### Sample Expected Output

**Console Output:**
```
Prompt: What are the best running shoes in 2025
Brand counts: Counter({'nike': 3, 'adidas': 2, 'hoka': 1, 'new balance': 1})

Prompt: Top performance sneakers for athletes
Brand counts: Counter({'nike': 4, 'adidas': 2, 'jordan': 1})

...

Results saved to brand_analysis_results.csv
```

**Generated CSV File (`brand_analysis_results.csv`):**
```csv
Prompt,Nike,Adidas,Hoka,New Balance,Jordan,Timestamp
What are the best running shoes in 2025,3,2,1,1,0,
Top performance sneakers for athletes,4,2,0,0,1,
Most comfortable sneakers for everyday wear,2,3,0,2,0,
Best shoes for marathon runners in 2025,1,1,3,2,0,
Top-rated basketball shoes this year,3,1,0,0,4,
What are the best shoes for trail running,2,1,2,1,0,
Best sneakers for flat feet,1,2,1,3,0,
Best lightweight shoes for speed workouts,3,2,1,1,0,
Most durable sneakers for heavy runners,2,1,1,2,0,
What are the trendiest sneakers in 2025,4,3,0,1,2,
```

## Stage 2: Mentions API

### Overview
Stage 2 provides a Flask API that serves brand mention metrics from a PostgreSQL database.

### How to Run Stage 2

1. **Set up PostgreSQL database**
   ```bash
   # Create database
   createdb bear_ai
   ```

2. **Navigate to the API directory**
   ```bash
   cd api
   ```

3. **Load CSV data into database**
   ```bash
   # Start the Flask app
   python app.py
   ```
   
   In another terminal, make a POST request to load the CSV data:
   ```bash
   curl -X POST http://localhost:8000/api/load-csv/
   ```

4. **API is now running at `http://localhost:8000`**

### API Endpoints

#### GET `/api/mentions/`
Returns total mentions for all brands.

**Sample Response:**
```json
{
  "count": 5,
  "mentions": [
    {
      "brand": "Nike",
      "mentions": 25
    },
    {
      "brand": "Adidas", 
      "mentions": 18
    },
    {
      "brand": "Jordan",
      "mentions": 7
    },
    {
      "brand": "New Balance",
      "mentions": 13
    },
    {
      "brand": "Hoka",
      "mentions": 10
    }
  ]
}
```

#### GET `/api/mentions/{brand_name}/`
Returns mention count for a specific brand.

**Example Request:**
```bash
curl http://localhost:8000/api/mentions/Nike/
```

**Sample Response:**
```json
{
  "brand": "Nike",
  "mentions": 25
}
```
## Next Steps

- Add better ways to bypass Cloudflare