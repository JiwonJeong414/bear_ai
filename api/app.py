import os
from db import db, BrandScore, load_brand_data_from_csv
from flask import Flask, jsonify
from dotenv import load_dotenv
from sqlalchemy import func

load_dotenv()

app = Flask(__name__)

# Database config
app.config.update(
    SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL'],
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_ECHO=True
)

db.init_app(app)

with app.app_context():
    db.create_all()

def success_response(data, status_code=200):
    """Helper method to return a success response"""
    return jsonify(data), status_code

def failure_response(error_message, status_code=500):
    """Helper method to return a failure response"""
    return jsonify({'error': error_message}), status_code

@app.route('/api/mentions/', methods=['GET'])
def get_brand_mentions():
    """Get total number of mentions for each brand"""
    try:
        # Query to get brand mention counts (where score > 0)
        brand_mentions = db.session.query(
            BrandScore.brand_name,
            func.sum(BrandScore.score).label('mention_count')
        ).filter(BrandScore.score > 0).group_by(BrandScore.brand_name).all()
        
        # Format the results
        mentions_data = [
            {
                'brand': brand_name,
                'mentions': mention_count
            }
            for brand_name, mention_count in brand_mentions
        ]
        
        # Sort by mention count (descending)
        mentions_data.sort(key=lambda x: x['mentions'], reverse=True)
        
        return success_response({
            'count': len(mentions_data),
            'mentions': mentions_data
        })
    except Exception as e:
        return failure_response(str(e))

@app.route('/api/mentions/<brand_name>/', methods=['GET'])
def get_brand_mention_count(brand_name):
    """Get mention count for a specific brand"""
    try:
        # Query to get mention count for specific brand (where score > 0)
        mention_count = db.session.query(
            func.sum(BrandScore.score)
        ).filter(
            BrandScore.brand_name == brand_name,
            BrandScore.score > 0
        ).scalar()
        
        return success_response({
            'brand': brand_name,
            'mentions': mention_count
        })
    except Exception as e:
        return failure_response(str(e))

@app.route('/api/load-csv/', methods=['POST'])
def load_csv_data():
    """Load brand analysis data from CSV file into database"""
    try:
        # Path to the CSV file from environment variable
        csv_file_path = os.environ['CSV_FILE_PATH']
        
        # Check if file exists
        if not os.path.exists(csv_file_path):
            return failure_response(f'CSV file not found at {csv_file_path}', 404)
        
        # Load data from CSV
        load_brand_data_from_csv(csv_file_path)
        
        # Get count of loaded records
        total_brand_scores = BrandScore.query.count()
        
        return success_response({
            'message': f'Successfully loaded {total_brand_scores} brand scores from CSV',
            'brand_scores_loaded': total_brand_scores,
            'file_path': csv_file_path
        })
        
    except Exception as e:
        db.session.rollback()
        return failure_response(str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
