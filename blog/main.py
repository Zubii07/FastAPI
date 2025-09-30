from fastapi import FastAPI, Depends, status, Response, HTTPException 
from . import schemas,models
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
@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create_blog(blog_post: schemas.BlogPost, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog_post.title, body=blog_post.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog', response_model=List[schemas.ShowBlog], status_code=200)
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code= 200,response_model=schemas.ShowBlog)
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Blog deleted"}


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, blog_post: schemas.BlogPost, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not available")
    blog.update({'title': blog_post.title, 'body': blog_post.body})
    db.commit()
    return {"detail": "Blog updated"}



@app.post('/user', status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=user.name, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f"User {user.name} created successfully"}
