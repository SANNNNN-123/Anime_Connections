from sqlalchemy import create_engine, Column, Integer, String, ARRAY, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.exc import IntegrityError
import os
import json


DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class OnePiece(Base):
    __tablename__ = "onepiece"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String,unique=False, index=True)
    category = Column(String, unique=True, index=True)
    words = Column(String)


def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # Data to be inserted
    data = [
        {"level": "easy", "category": "New Yonkou", "words": ["Shanks", "Luffy", "Buggy", "BlackBeard"]},
        {"level": "easy", "category": "Logia Fruit", "words": ["Enel", "Kuzan", "Sabo", "Crocodile"]},
        {"level": "easy", "category": "Swordsmen", "words": ["Brooke", "Kuina", "Mihawk", "Killer"]},
        {"level": "easy", "category": "Marines", "words": ["Smoker", "Garp", "Sengoku", "Tashigi"]},
        {"level": "easy", "category": "Revolutionary Army", "words": ["Dragon", "Sabo", "Koala", "Kuma"]},
        {"level": "easy", "category": "Bounty Hunters", "words": ["Zeff", "Dadan", "Sentomaru", "Zoro"]},
        {"level": "easy", "category": "Fishman", "words": ["Arlong", "Hachi", "Jinbe", "FisherTiger"]},
        {"level": "easy", "category": "Impel Down", "words": ["Magellan", "Saldeath", "Shiryu", "Ivankov"]},
        {"level": "easy", "category": "Haki Types", "words": ["Armament", "Observation", "Conqueror", "Advanced"]},
        {"level": "easy", "category": "Straw Hat Pirates", "words": ["Franky", "Chopper", "Nami", "Usopp"] },
        {"level": "easy", "category": "Worst Generation", "words": ["Bonney", "Bege", "Kid", "Law"] },
        {"level": "easy", "category": "Admirals", "words": ["Kizaru", "Akainu", "Ryokugyu", "Fujitora"] },
        {"level": "easy", "category": "Wano Nine Red Scabbards", "words": ["Kinemon", "Kanjuro", "Kiku", "Raizo"] },
        {"level": "easy", "category": "Dressrosa", "words": ["Doflamingo", "Riku", "Viola", "Kyros"]},

        # Medium Level
        {"level": "medium", "category": "Fire Users", "words": ["Ace", "Sabo", "Akainu", "Oven"]},
        {"level": "medium", "category": "Revolutionary Army", "words": ["Dragon", "Inazuma", "Ivankov", "Koala"]},
        {"level": "medium", "category": "Will of D", "words": ["Luffy", "Vivi", "Cobra", "Xebec"]},
        {"level": "medium", "category": "Royal Bloodline", "words": ["Donflamigo", "Sanji", "Kuma", "Hancock"]},

        {"level": "medium", "category": "Yonko", "words": ["Luffy", "Teach", "Buggy", "Shanks"]},
        {"level": "medium", "category": "Warlord", "words": ["Weevil", "Mihawk", "Jinbei", "Kuma"]},
        {"level": "medium", "category": "Worst Generation", "words": ["Law", "Zoro", "Hawkins", "Kid"]},
        {"level": "medium", "category": "Lost to Luffy", "words": ["Doflamingo", "Crocodile", "Moria", "Kaido"]},
        
        {"level": "medium", "category": "Swords User", "words": ["Mihawk", "Kuma", "Crocodile", "Jinbe"] },
        {"level": "medium", "category": "Time Travel", "words": ["Kouzuki Toki", "Momonosuke","Raizo","Kanjuro"] },
        {"level": "medium", "category": "RedHair Pirates", "words": ["Shanks", "Lucky Roux", "Yasopp","Benn Beckman"] },
        {"level": "medium", "category": "Mink Tribe", "words": ["Bepo", "Pedro","Carrot","Nekomamushi"] },
        
        {"level": "medium", "category": "Roger's Crew", "words": ["Roger", "Rayleigh", "Crocus", "Buggy"] },
        {"level": "medium", "category": "Rock Pirates", "words": ["Kaido", "Xebec", "Whitebeard", "Shiki"] },
        {"level": "medium", "category": "Yonkou", "words": ["Shanks", "Teach", "Big Mom", "Blackbeard"] },
        {"level": "medium", "category": "Conqueror's Haki", "words": ["Luffy", "Rayleigh", "Zoro", "Whitebeard"]},

        {"level": "medium", "category": "Freeze", "words": ["Aokiji", "Monet", "Yamato", "Brooke"] },
        {"level": "medium", "category": "Fly", "words": ["Bellamy", "King", "Perona", "Marco"] },
        {"level": "medium", "category": "Heart Pirate", "words": ["Law", "Bepo", "Penguin", "Jean Bart"] },
        {"level": "medium", "category": "Teleportation", "words": ["Van Augur", "Kizaru","Kuma","Blueno"]},


        # Hard Level
        {"level": "hard", "category": "Devil Fruit Science", "words": ["Lineage", "SMILE", "Awakening", "Artificial"]},
        {"level": "hard", "category": "Void Century", "words": ["Ohara", "Scholars", "Research", "Knowledge"]},
        {"level": "hard", "category": "World Nobles", "words": ["Celestial", "Dragons", "Mariejois", "Royalty"]},
        {"level": "hard", "category": "Revolutionary Bases", "words": ["Baltigo", "Kamabakka", "Momoiro", "Newkama"]},
        {"level": "hard", "category": "Ancient Technology", "words": ["Vegapunk", "Lineage", "Factor", "Cloning"]},
        {"level": "hard", "category": "Secret Organizations", "words": ["SWORD", "SHIELD", "CP0", "Cipher"]},
        {"level": "hard", "category": "Will of D", "words": ["Mystery", "Ancient", "Heritage", "Destiny"]},
        {"level": "hard", "category": "Lost History", "words": ["Lunarians", "Shandians", "Skypiea", "Birka"]}
    ]

    

    # Insert data
    for item in data:
        try:
            # Include level when creating the OnePiece object
            db_item = OnePiece(
                level=item["level"],  # Add this line
                category=item["category"], 
                words=str(item["words"])  # Convert list to string
            )
            db.merge(db_item)
            db.commit()
        except IntegrityError:
            db.rollback()
            existing_item = db.query(OnePiece).filter(OnePiece.category == item["category"]).first()
            if existing_item:
                existing_item.level = item["level"]  # Update level
                existing_item.words = str(item["words"])  # Update words
                db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error processing {item['category']}: {str(e)}")

    print("Database initialized and data inserted.")
    db.commit()
    db.close()

def insert_data_from_json(json_file_path):
    """
    Insert data from a JSON file into the database.
    
    :param json_file_path: Path to the JSON file containing data to insert
    """
 
    # Open and load the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    # Create a database session
    db = SessionLocal()
    
    # Insert data
    for item in data:
        try:
            # Create a new OnePiece object
            db_item = OnePiece(
                level=item.get("level", ""),  # Use get() to provide a default value if level is missing
                category=item["category"], 
                words=str(item["words"])  # Convert list to string
            )
            
            # Use merge to update existing records or insert new ones
            db.merge(db_item)
            db.commit()
        
        except IntegrityError:
            # Handle potential integrity errors
            db.rollback()
            
            # Try to update existing record
            existing_item = db.query(OnePiece).filter(OnePiece.category == item["category"]).first()
            if existing_item:
                existing_item.level = item.get("level", existing_item.level)
                existing_item.words = str(item["words"])
                db.commit()
        
        except Exception as e:
            # Rollback and print error for any other exceptions
            db.rollback()
            print(f"Error processing {item.get('category', 'Unknown')}: {str(e)}")
    
    print("Data from JSON file inserted successfully.")
    db.close()

def get_onepiece_data(difficulty='easy'):
    db = SessionLocal()
    try:
        if difficulty:
            data = db.query(OnePiece)\
                .filter(OnePiece.level == difficulty)\
                .order_by(func.random())\
                .limit(4)\
                .all()
        else:
            data = db.query(OnePiece).all()
        
        return [{"level": item.level, "category": item.category, "words": eval(item.words)} 
                for item in data]
        

    finally:
        db.close()

def get_new_onepiece_data(difficulty='easy', db: Session = None):
    if db is None:
        db = SessionLocal()
    
    try:
        # Set to track all words to prevent duplicates
        used_words = set()
        selected_data = []
        
        # Maximum attempts to find unique categories
        max_attempts = 10
        attempts = 0
        
        while len(selected_data) < 4 and attempts < max_attempts:
            # Query for a random category at the specified difficulty
            category_query = db.query(OnePiece)\
                .filter(OnePiece.level == difficulty)\
                .order_by(func.random())\
                .first()
            
            if not category_query:
                break
            
            # Convert words to a list and check for duplicates
            current_words = eval(category_query.words)
            
            # Check if any word is already used
            if not any(word in used_words for word in current_words):
                # Add words to used_words set
                used_words.update(current_words)
                
                # Add this category to selected data
                selected_data.append({
                    "level": category_query.level, 
                    "category": category_query.category, 
                    "words": current_words
                })
            
            attempts += 1
        
        # If we couldn't find 4 unique categories, return what we found
        return selected_data

    except Exception as e:
        print(f"Error in get_new_onepiece_data: {e}")
        return []
    finally:
        if db:
            db.close()


def get_ALL_data():
    db = SessionLocal()
    try:
        data = db.query(OnePiece).all()
        return [{"level": item.level , "category": item.category, "words": item.words} for item in data]
    finally:
        db.close()
  
    