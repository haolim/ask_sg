from ask_sg.core.database import SessionLocal

def get_db():
    # Open connection on demand, only when a request actually needs the DB
    db = SessionLocal()

    try:
        yield db # request uses it
    finally:
        db.close() # closes after request is fully done