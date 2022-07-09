from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#define postgresql connection url
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost/item_db"
SQLALCHEMY_DATABASE_URL = "postgresql://ecuiicbpetakuf:64e2a8466fac4b86713479f158c73544c7f0e22a7009739c7e7a907c9bcf0b68@ec2-34-233-115-14.compute-1.amazonaws.com:5432/dio6le8v94ihv"

# create new engine instance 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create sessionmaker 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()