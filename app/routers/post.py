from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
# from fastapi.params import Body
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
# from sqlalchemy import or_
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user : schemas.User = Depends(oauth2.get_current_user), limit : int = 10, skip : int = 0, search : Optional[str] = ''):
    # posts = db.query(models.Post).filter(
    #     or_(
    #         models.Post.published==True, 
    #         models.Post.user_id == current_user.id
    #         )
    #     ).all()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # return{'Data': posts}
    return result

# def get_posts():
#     cursor.execute("""
#     SELECT * FROM posts
#     """)
#     post = cursor.fetchall()
#     print(post)
#     # print(dict(post)) # it do not work it throw an error
#     return {'Data': post}
# def get_posts():
#     return {'Data': my_posts}
# def get_posts():
#     return {'Data': 'This is your posts'}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post : schemas.PostCreate, db : Session = Depends(get_db), current_user : schemas.User = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=post.title, content = post.content, published = post.published)
    print(current_user.password)
    new_post = models.Post(**post.dict(), user_id = current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # return {'Data': new_post}
    return new_post

# def create_posts(post :Post):
#     # cursor.execute(
#     # f"""
#     # INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content}, {post.published})
#     # """
#     # ) # will work but you are vulnerable to sql injection

#     cursor.execute(
#     """
#     INSERT INTO posts (title, content, published) 
#     VALUES (%s, %s, %s)
#     RETURNING *
#     """, 
#     (post.title, post.content, post.published)
#     )
#     new_post = cursor.fetchone()
#     conn.commit()
#     print(new_post)
#     return {'data': new_post}
# def create_posts(post :Post):
#     id = my_posts[-1]['id']
#     post_dict = post.dict()
#     post_dict['id'] = id + 1
#     my_posts.append(post_dict)
#     # print(post)
#     # print(post.dict())
#     # print(post)
#     return {'data': post_dict}
# def create_posts(new_post :Post):
#     print(new_post.rating)
#     return {'data': f"Title: {new_post.title} Content: {new_post.content}"}
# def create_posts(payload: dict = Body()):
#     print(payload)
#     return {'new_post': f"Title: {payload['title']} Content: {payload['content']}"}

# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id : int, db : Session = Depends(get_db), current_user : schemas.User = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(
    #     models.Post.id == id, 
    #     or_(
    #         models.Post.published == True, 
    #         models.Post.user_id == current_user.id
    #         )
    #     ).first()
    post = db.query(
            models.Post, 
            func.count(models.Vote.post_id).label("votes")
        ).join(
            models.Vote, 
            models.Post.id == models.Vote.post_id,
            isouter=True
        ).group_by(
            models.Post.id
        ).filter(
            models.Post.id == id
        ).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with id {id} was not found")
    # return {'Data' : post}
    return post

# def get_post(id : int):
#     cursor.execute(
#         """
#         SELECT * FROM posts WHERE id = %s
#         """, (str(id),)
#     )
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with id {id} was not found")

#     return {'data': post}
# def get_post(id : int):
#     try:
#         cursor.execute(
#         """
#         SELECT * FROM posts WHERE id = %s
#         """, str(id)
#         )
#         post = cursor.fetchone()
#     except:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with id {id} was not found")

#     return {'data': post}
# def get_post(id : int):
#     post = find_post(id)
#     # assert post, HTTPException(status.HTTP_404_NOT_FOUND, f"Post with id {id} was not found") # wound not work bcos it will throw an error in my text editor

#     if not post:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with id {id} was not found")

#     return {'data': post}
# def get_post(id : int, reponse: Response):
#     # for i in range(len(my_posts)):
#     #     if int(id) == my_posts[i]["id"]:
#     #         the_post = my_posts[i]
#     #         break
#     # else:
#     #     the_post = "No post available"
#     post = find_post(id)
#     if not post:
#         reponse.status_code = status.HTTP_404_NOT_FOUND
#         return {
#             "Message": f"Post with id {id} was not found"
#         }

#     return {'data': post}
#     # return {'data': the_post}
#     # return {'data': f"Here is post with id {id}"}


# def find_index_post(id):
#     for i in range(len(my_posts)):
#         if id == my_posts[i]["id"]:
#             return i
    
        
# @app.delete('posts/{id}')
# def delete_post(id: int):
#     # index = find_index_post(id)
#     # print(index)
#     # my_posts.pop(index)
#     # del(my_posts[index])

#     return {'Message': 'Post was successfully deleted'}


@router.delete('/{id}')
def delete_post(id : int, db : Session = Depends(get_db), current_user : schemas.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with id {id} does not exist")
    if post.first().user_id != current_user.id:
        raise HTTPException(status.HTTP_402_PAYMENT_REQUIRED, f"Not authorized to preform required action")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# def delete_post(id: int):
#     cursor.execute(
#         """
#         DELETE FROM posts WHERE id = %s
#         RETURNING *
#         """, (str(id),)
#     )
#     delete_post = cursor.fetchone()
#     if not delete_post:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with id {id} was not exist")
#     conn.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     try:
#         cursor.execute("""
#     DELETE FROM posts WHERE id = %s
#     """, str(id))
#     except:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with id {id} was not exist")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# def delete_post(id: int):
#     index = find_index_post(id)
#     if index == None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with id {id} does not exist")
#     my_posts.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.Post)
def update_post(id : int, post : schemas.PostCreate, db : Session = Depends(get_db), current_user : schemas.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id) 
    if not post_query.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with id {id} does not exist")
    
    if post_query.first().user_id != current_user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Not authorized to preform required action")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    # return{"Data": post_query.first()}
    return post_query.first()


# def update_post(id: int, post: Post):
#     cursor.execute(
#         """
#         UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s
#         RETURNING *
#         """, (post.title, post.content, post.published, str(id))
#     )
#     update_post = cursor.fetchone()
#     if not update_post:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with id {id} does not exist")
#     conn.commit()
#     return{"Data": update_post}

# def update_post(id: int, post: Post):
#     index = find_index_post(id)
#     if index == None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with id {id} does not exist")
#     post_dict = post.dict()
#     post_dict['id'] = id
#     my_posts[index] = post_dict
#     print(my_posts)
#     return {
#         'Data': post_dict
#     }
