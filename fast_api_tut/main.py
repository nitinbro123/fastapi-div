from fastapi import FastAPI,Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
app=FastAPI()

# title str,content str, category,
class post(BaseModel):
    title: str
    content:str
    published:bool=True
    rating:Optional[int]=None

my_post=[{"title":"title of post 1","content": "content of post 1","id":1},{"title":"faverate foods","content":"i like piza","id":2}]

def find_post(id):
    for p in my_post:
        if p["id"]==id:
            return p
    return None


@app.get("/")
async def root():
    return{"message":"hello nitin"}

@app.get("/post")
def get_posts():
    return{"Data":my_post}

# add data with old existing data
@app.post("/post")
def Create_post(post:post):
    post_dict=post.model_dump()
    post_dict['id']=randrange(0,1000000)
    my_post.append(post_dict)
    #print(post .model_dump()) #Ye class se bane object (addpost) ka data dictionary mein nikalta hai.
    return{"data":post_dict}

#cheak latest post
@app.get("/post/latest")
def get_latest_post():
    if not my_post:
        return {"message": "No posts available"}

    latest = my_post[-1]
    return {"details": latest}


#get retrive
@app.get("/post/{id}")
def get_post(id: int,response:Response):
    post=find_post((id))
    if not post:
        response.status_code=404# if we not yous it's give 200 it's mean successful found !
        return{"message":"post not found"}
    return{"data":post}


# delete all spacific post
@app.delete("/post/{id}")
def delete_post(id:int):
    for post in my_post:
        if post["id"]==id:
            my_post.remove(post)
            return{"message":f"post{post["id"]}:delete"}
    return{"message":"post not found"}
