import os
import string
import urllib
import uuid
import pickle
import datetime
import time
import shutil

import cv2
from fastapi import FastAPI, File, UploadFile, Form, UploadFile, Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import face_recognition
import starlette

from fastapi import  Depends,HTTPException,status,Response
from sqlalchemy.orm import Session
from config.database import get_db
from models.people import People
from models.assists import Assists
from schemas.people_schema import PeopleCreateSchema,PeopleSchema
from schemas.assists_schema import AssistsCreateSchema,AssistsSchema

ATTENDANCE_LOG_DIR = './logs'
DB_PATH = './db'
for dir_ in [ATTENDANCE_LOG_DIR, DB_PATH]:
    if not os.path.exists(dir_):
        os.mkdir(dir_)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/login")
async def login(file: UploadFile = File(...), db: Session = Depends(get_db)):

    file.filename = f"{uuid.uuid4()}.png"
    contents = await file.read()

    # example of how you can save the file
    with open(file.filename, "wb") as f:
        f.write(contents)

    people_id, match_status = recognize(cv2.imread(file.filename))

    if match_status:
        people_query = db.query(People).filter(People.id == people_id)
        db_people= people_query.first()

        assists_schema=AssistsCreateSchema(arrivaltime=datetime.datetime.now(),people_id=db_people.id)
        new_assist=Assists(**assists_schema.dict())
        db.add(new_assist)
        db.commit()
        db.refresh(new_assist)

        people_query = db.query(People).filter(People.id == people_id)
        db_people= people_query.first()
        os.remove(file.filename)

    return {'user': db_people, 'match_status': match_status}


@app.post("/logout")
async def logout(file: UploadFile = File(...)):

    file.filename = f"{uuid.uuid4()}.png"
    contents = await file.read()

    # example of how you can save the file
    with open(file.filename, "wb") as f:
        f.write(contents)

    user_name, match_status = recognize(cv2.imread(file.filename))

    if match_status:
        epoch_time = time.time()
        date = time.strftime('%Y%m%d', time.localtime(epoch_time))
        with open(os.path.join(ATTENDANCE_LOG_DIR, '{}.csv'.format(date)), 'a') as f:
            f.write('{},{},{}\n'.format(user_name, datetime.datetime.now(), 'OUT'))
            f.close()

    return {'user': user_name, 'match_status': match_status}


@app.post("/register_new_user")
async def register_new_user(file: UploadFile = File(...), text=None, db: Session = Depends(get_db)):

    
    
    file.filename = f"{uuid.uuid4()}.png"
    contents = await file.read()

    # example of how you can save the file
    with open(file.filename, "wb") as f:
        f.write(contents)
    
    user_name, match_status = recognize(cv2.imread(file.filename))

    if match_status:
        os.remove(file.filename)
        return {'registration_status': 404}
    else:
     people_schema=PeopleCreateSchema(name="Balmore",lastname="Cruz",carnet="CV100121",image="",role_id=1)
     new_people=People(**people_schema.dict())
     db.add(new_people)
     db.commit()
     db.refresh(new_people)

     shutil.copy(file.filename, os.path.join(DB_PATH, '{}.png'.format(new_people.id)))
 
     embeddings = face_recognition.face_encodings(cv2.imread(file.filename))
 
     file_ = open(os.path.join(DB_PATH, '{}.pickle'.format(new_people.id)), 'wb')
     pickle.dump(embeddings, file_)
     print(file.filename, text)
 
     os.remove(file.filename)
 
     return {'registration_status': 200}


@app.get("/get_attendance_logs")
async def get_attendance_logs():

    filename = 'out.zip'

    shutil.make_archive(filename[:-4], 'zip', ATTENDANCE_LOG_DIR)

    ##return File(filename, filename=filename, content_type="application/zip", as_attachment=True)
    return starlette.responses.FileResponse(filename, media_type='application/zip',filename=filename)


@app.post("/people")
async def createPeople(people: PeopleCreateSchema, db: Session = Depends(get_db)):
  
    new_people=People(**people.dict())
    db.add(new_people)
    db.commit()
    db.refresh(new_people)
    return {"result":new_people}


@app.get("/people")
async def getAllPeople(db: Session = Depends(get_db)):
    people=[];
    data = db.query(People).filter().all()
    for d in data:
        item=PeopleSchema(id=d.id,name=d.name,lastname=d.lastname,carnet=d.carnet,image=d.image,role=d.role)
        people.append(item)
    return {'result':people}


@app.get("/assists")
async def getAllAssists(db: Session = Depends(get_db)):
    assists=[];
    data = db.query(Assists).filter().all()
    for d in data:
        item=AssistsSchema(id=d.id,arrivaltime=d.arrivaltime,people=d.people)
        assists.append(item)
    return {'result':assists}


def recognize(img):
    # it is assumed there will be at most 1 match in the db
    embeddings_unknown = face_recognition.face_encodings(img)
    if len(embeddings_unknown) == 0:
        return 'no_persons_found', False
    else:
        embeddings_unknown = embeddings_unknown[0]

    match = False
    j = 0

    db_dir = sorted([j for j in os.listdir(DB_PATH) if j.endswith('.pickle')])
    # db_dir = sorted(os.listdir(DB_PATH))    
    print(db_dir)
    while ((not match) and (j < len(db_dir))):

        path_ = os.path.join(DB_PATH, db_dir[j])

        file = open(path_, 'rb')
        embeddings = pickle.load(file)[0]

        match = face_recognition.compare_faces([embeddings], embeddings_unknown)[0]

        j += 1

    if match:
        return db_dir[j - 1][:-7], True
    else:
        return 'unknown_person', False


