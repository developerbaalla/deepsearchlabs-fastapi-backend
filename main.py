from fastapi import FastAPI, HTTPException

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

