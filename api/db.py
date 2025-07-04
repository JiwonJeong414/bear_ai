from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate
import csv

db = SQLAlchemy()

class BrandScore(db.Model):
    """
    BrandScore Model that represents a brand's score
    """
    __tablename__ = "brand_score"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand_name = db.Column(db.Text, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<BrandScore {self.brand_name}: {self.score}>'

def load_brand_data_from_csv(csv_file_path):
    """Load brand analysis data from CSV file into database"""
    # Clear existing data
    BrandScore.query.delete()
    db.session.commit()
    
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Get brand names from header (excluding 'Prompt')
        brand_names = [col for col in reader.fieldnames if col != 'Prompt']
        
        for row in reader:
            # Create brand score records for this prompt
            for brand_name in brand_names:
                score = int(row[brand_name])
                
                brand_score_record = BrandScore(
                    brand_name=brand_name,
                    score=score
                )
                db.session.add(brand_score_record)
        
        db.session.commit()



    