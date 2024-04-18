from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# import psycopg2
# from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
from .routers import user, post, auth, vote
from .config import Setting

# models.Base.metadata.create_all(bind=engine) #this what create all of tables when we havve not started using alembic

app = FastAPI()

# origins = [
#     "https://www.ebay.com",
#     "https://www.google.com",
#     "https://www.youtube.com"
# ]

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True,
)

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Juel', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful!")
#         break
#     except Exception as error:
#         print("connecting to database failed")
#         print('Error: ', error)
#         time.sleep(2)

# my_posts = [
#     {
#         "title": "title of post 1",
#         "content": "content of post 2",
#         "id": 1
#      },
#      {
#          "title": "favorite food",
#          "content": "I like pizza",
#          "id": 2
#      }
# ]

@app.get('/')
def root():
    return {'Message': "Welcome to my api!!!!"}

# @app.get('/sqlalchemys')
# def test_posts(db: Session = Depends(get_db)):
#     post = db.query(models.Post).all()
#     return {'Data': post}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)