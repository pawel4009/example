
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session
from app import models, schemas
from app.routers import oauth2
from app.database import get_db
from typing import Optional

# prefix; we dont have write "/posts" in all path oper
# tags: documentation is divided
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# API server will look only at the first match
# sql statement
# validation of the incomming info from the postgresql database
@router.get("/", response_model=List[schemas.PostOut]) # validation of the incomming info from the postgresql database
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""): # we have to set {{URL}}posts?limit=5&skip=2 in postman
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # set limit
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #.filter(models.Post.owner_id == current_user.id) - we want to only fetch posts that belong to us

    # we want to perform left join (by deafult in sqlalchemy we have left outer join). In SQL it would be: SELECT posts.id, COUNT(votes.post_id) FROM posts LEFT JOIN votes ON votes.post_id = posts.id GROUP BY posts.id
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(list(results))

    return results


# SQL
# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post: Post):
#     # never do this with f-strings, because someone can create sql injection, psycopg2 takes care of this with %s
#     cursor.execute(""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * "", (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     # it will push these changes to the database
#     conn.commit()
#     return {"data": new_post}


# ORM
# post: schemas.PostCreate  is used to valide user input, so the response
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# get_current_user - this function now is going to be dependency, if someone wants to create post, he will need to be logged in
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # we need to provide user's post id 
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/latest", response_model=schemas.PostOut) # order of the path parameters matters
def get_latest_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    return post



# SQL
# @app.get("/posts/{id}") # id represents path parameter
# def get_post(id: int):
#     cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": f"cannot find post with id: {id}"})
#     return {"post_details": post}


# ORM
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": f"cannot find post with id: {id}"})
    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    return result


# SQL
# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute("""DELETE FROM posts WHERE ID = %s RETURNING *""", (str(id),))
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     if not deleted_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
#     # is it really necessary?
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# ORM
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# SQL
# @app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
# def update_post(id: int, post: Post):
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
#                    (post.title, post.content, post.published, str(id)))
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if not updated_post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
#     return {"data": updated_post}


# ORM
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()