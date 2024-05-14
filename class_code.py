from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import cv2
import numpy as np
import io  # Defult Python


app = FastAPI()
friends = {}

@app.get("/items")
def read_friends():
    return friends

@app.post("/items")  #inssert  
def add_friend(id: str = Form(), name: str = Form(), age: float = Form()):
    friends[id] = {"name": name, "age": age}

    return friends[id]

@app.delete("/items/{id}")  #delete  
def remove_friend(id: str):
    if id not in friends:
        raise HTTPException(status_code=404, detail="item not found")
    del friends[id]

    return {"Message": "item deleted"}   

@app.put("/items/{id}")  #update  
 
def update_friend(id: str, name: str = Form(None), age: float = Form(None)):
    if id not in friends:
        raise HTTPException(status_code=404, detail="item not found")
    if name is not None:
        friends[id]["name"] = name
    if age is not None:
        friends[id]["age"] = age    

    return friends[id]

@app.post("/rgb2gray") 
async def rgb2gray(input_file: UploadFile = File(None)):
    if not input_file.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail="Unsuported File Type...")
    contents = await input_file.read()
    np_array = np.frombuffer(contents, dtype=np.uint8) 
    image_rgb = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED) 
    # cv2.imwrite("test.jpg", image_rgb) 

    #process 
    image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)

    _, encoded_image = cv2.imencode(".jpg", image_gray) 
    image_bytes = encoded_image.tobytes()
    return StreamingResponse(io.BytesIO(image_bytes), media_type="image/jpeg") 

    


     



