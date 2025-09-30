from fastapi import FastAPI, Depends, status, Response, HTTPException 
from . import schemas,models,hashing
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()


models.Base.metadata.create_all(engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=["Blogs"])
def create_blog(blog_post: schemas.BlogPost, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog_post.title, body=blog_post.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog', response_model=List[schemas.ShowBlog], status_code=200,tags=["Blogs"])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code= 200,response_model=schemas.ShowBlog, tags=["Blogs"])
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Blogs"])
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Blog deleted"}


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["Blogs"])
def update(id, blog_post: schemas.BlogPost, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
    blog.update({'title': blog_post.title, 'body': blog_post.body})
    db.commit()
    return {"detail": "Blog updated"}



@app.post('/user', response_model=schemas.ShowUser,status_code=status.HTTP_201_CREATED,tags=["Users"])
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    new_user = models.User(name=user.name, email=user.email, password=hashing.Hash.argon2(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f"User {user.name} created successfully"}
