from sqlalchemy import create_engine, Column, Integer, String, ARRAY, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.exc import IntegrityError
import os


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
        
        {"level": "easy", "category": "Straw Hat Pirates", "words": ["Franky", "Chopper", "Nami", "Usopp"] },
        {"level": "easy", "category": "Worst Generation", "words": ["Bonney", "Bege", "Kid", "Law"] },
        {"level": "easy", "category": "Admirals", "words": ["Kizaru", "Akainu", "Aokiji", "Fujitora"] },

        # Medium Level
        {"level": "medium", "category": "Devil Fruit Types", "words": ["Paramecia", "Zoan", "Logia", "Mythical"]},
        {"level": "medium", "category": "Ancient Weapons", "words": ["Pluton", "Poseidon", "Uranus", "Neptune"]},
        {"level": "medium", "category": "Poneglyphs", "words": ["Rio", "Road", "Historic", "Ancient"]},
        {"level": "medium", "category": "Haki Types", "words": ["Armament", "Observation", "Conqueror", "Advanced"]},
        {"level": "medium", "category": "Pirate Crews", "words": ["Strawhats", "Redhair", "Whitebeard", "Blackbeard"]},
        {"level": "medium", "category": "Grand Line", "words": ["Paradise", "NewWorld", "Sabaody", "Fishman"]},
        {"level": "medium", "category": "World Government", "words": ["Cipher", "Gorosei", "ImSama", "CP9"]},
        {"level": "medium", "category": "Ancient Kingdom", "words": ["Void", "Century", "DGreat", "Kingdom"]},
        
        {"level": "medium", "category": "Shichibukai", "words": ["Mihawk", "Kuma", "Crocodile", "Jinbe"] },
        {"level": "medium", "category": "Members of CP9", "words": ["Lucci", "Kaku", "Blueno", "Jabura"] },
        {"level": "medium", "category": "Dressrosa Rulers", "words": ["Doflamingo", "Riku", "Viola", "Kyros"]},
        {"level": "medium", "category":"Wano Nine Red Scabbards", "words": ["Kinemon", "Kanjuro", "Kiku", "Raizo"] },


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
        # Query for specific difficulty and get 4 random categories
        data = db.query(OnePiece)\
            .filter(OnePiece.level == difficulty)\
            .order_by(func.random())\
            .limit(4)\
            .all()
        
        return [{"level": item.level, "category": item.category, "words": eval(item.words)} 
                for item in data]
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
  
    