from fastapi import FastAPI, HTTPException
import models
from csv import reader
from db import engine
from sqlalchemy.orm import Session, joinedload, contains_eager
from fastapi.middleware.cors import CORSMiddleware
import json

#create the database tables on app startup or reload
models.Base.metadata.create_all(bind=engine)

#initailize FastApi instance
app = FastAPI()

# origins = ["*"]

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=origins,
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

@app.get("/")
def home():
    return {'message': 'this is the root message'}

#count_sentence endpoint
#return the count sentences
@app.get("/count_sentence")
def count_sentence(sentence: str = '', keyword: str = ''):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)
    
    try:
        # get count_sentences
        if sentence != '':
            count_sentences = session.query(models.Sentence.id).filter(models.Sentence.sentence.ilike(f'%{sentence}%')).count()
        elif keyword != '':
            count_sentences = session.query(models.Sentence.id).join(models.Sentence.sentence_keywords).options(contains_eager(models.Sentence.sentence_keywords)).filter(models.SentenceKeyword.value.ilike(f'%{keyword}%')).count()
        else:
            count_sentences = session.query(models.Sentence.id).options(joinedload(models.Sentence.sentence_keywords)).count()

    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

    finally:
        # close the session
        session.close()

    return count_sentences


#sentence_keywords endpoint
#return the sentence tabel and associated keywords
@app.get("/sentence_keywords")
def sentence_keywords_list(sentence: str = '', keyword: str = '', page: int = 1, limit: int = 10):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    try:
        # get sentence_keywords items
        if sentence != '':
            sentence_keywords = session.query(models.Sentence).options(joinedload(models.Sentence.sentence_keywords)).filter(models.Sentence.sentence.ilike(f'%{sentence}%')).order_by(models.Sentence.id.desc()).offset((page - 1) * limit).limit(limit).all()
        elif keyword != '':
            sentence_keywords = session.query(models.Sentence).join(models.Sentence.sentence_keywords).options(contains_eager(models.Sentence.sentence_keywords)).filter(models.SentenceKeyword.value.ilike(f'%{keyword}%')).order_by(models.Sentence.id.desc()).offset((page - 1) * limit).limit(limit).all()
        else:
            sentence_keywords = session.query(models.Sentence).options(joinedload(models.Sentence.sentence_keywords)).order_by(models.Sentence.id.desc()).offset((page - 1) * limit).limit(limit).all()

    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

    finally:
        # close the session
        session.close()

    return sentence_keywords


#young_people endpoint
#return the the logits and some other information
@app.get("/young_people")
def young_people_list():
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    try:
        # get all young_people items
        young_people_list = session.query(models.YoungPeople).with_entities(models.YoungPeople.id, models.YoungPeople.date, models.YoungPeople.logits, models.YoungPeople.net_sent, models.YoungPeople.logits_mean).order_by(models.YoungPeople.date.asc()).all()

    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

    finally:
        # close the session
        session.close()

    return young_people_list



@app.get("/add_sentence", response_description="Sentence data added into the database")
async def add_sentence():

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    data = []

    try:
        
        # open file
        with open("genZ.csv", "r", encoding='utf-8') as my_file:
            # pass the file object to reader()
            file_reader = reader(my_file)
            # do this for all the rows
            for i in file_reader:
                # print the rows
                _keywords = i[5].replace('\\', "").replace("'", '\"')
                _keywords = json.loads(_keywords)
                _keywords = [ x[0] for x in _keywords]
                data.append([i[3], _keywords])


        for _sentence in data:
        
            # Add keywords ---------------------------------------
            new_keywords = []
            for _keyword in _sentence[1]:
                new_keyword = models.SentenceKeyword()
                new_keyword.value = _keyword[0:250]
                session.add(new_keyword)
                session.flush()
                new_keywords.append(new_keyword)

            # Add sentence ---------------------------------------
            new_sentence = models.Sentence()
            new_sentence.sentence = _sentence[0]
            for k in new_keywords:
                new_sentence.sentence_keywords.append(k)
            session.add(new_sentence)
            session.flush()

        session.commit()
        session.close()

    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

    finally:
        # close the session
        session.close()

    return data