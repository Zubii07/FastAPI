from fastapi import FastAPI, Depends, status, Response
from . import schemas,models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
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


@app.get('/blog')
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}')
def get_blog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": "Blog not found"}
    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)

    db.commit()
    return {"detail": "Blog deleted"}
