from app import db

db.create_all()

db.execute("CREATE TABLE IF NOT EXISTS keywords (keyword text)") 

db.execute("INSERT INTO keywords (keyword) VALUES ('insulin')")

db.commit()