import re
import uvicorn
import motor.motor_asyncio
import json
from bson import ObjectId
from typing import Optional, List
from pydantic import BaseModel, Field
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://121.0.0.1:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URI='mongodb://localhost:27017'
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.supplements


class PyObjectId(ObjectId):
    """ Custom Type for reading MongoDB IDs """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid object_id")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class ProteinModel(BaseModel):
    producer: Optional[str]
    name: Optional[str]
    weight: Optional[float]
    price: Optional[float]
    old_price: Optional[float]
    discount: Optional[float]
    price_standarized: Optional[float]
    image: Optional[str]
    url: Optional[str]
    date_added: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}



class ProteinOutModel(ProteinModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config(ProteinModel.Config):
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class ProteinInModel(ProteinModel):
    class Config(ProteinModel.Config):
        schema_extra = {
            "example":{   
                "producer": "New",
                "name": "New Protein-700g",
                "weight": 700,
                "price": 99.99,
                "old_price": None,
                "discount": None,
                "price_standarized": 14.28,
                "image": "https://s3.sbodypak.pl/img/p/3/1/4/5/4/31454-home_default.jpg",
                "url": "https://www.bodypak.pl/pl/odzywki-bialkowe/17289-trec-endurance-high-protein-shake-waniliowy-700g.html",
                "date_added": "2022-05-23"
            }
        }

class ProteinsResponseModel(BaseModel):
    results: List[ProteinOutModel]
    count: int

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)


@app.get('/')
def index():
    return 'Index'


@app.get("/producers/", response_description="List All Producer", response_model=List[str])
async def list_produces():
    return await db["proteins"].distinct('producer')


@app.get("/protein/{id}", response_description="Get Protein With Given Id", response_model=ProteinOutModel)
async def protein(id:str):
    if (protein := await db["proteins"].find_one({"_id": ObjectId(id)})) is not None:
        return protein

    raise HTTPException(status_code=404, detail=f"Protein {id} not found")


@app.get("/proteins/", response_description="List of Filtered Proteins", response_model=ProteinsResponseModel)
async def list_proteins(
    page: int = 1, 
    limit: int = 10,
    name: str | None = None,
    producer: str | None = None,
    date_added: str | None = None,
    sort: str  = '_id.desc',
):
    filter_keys = {'name': name, 'producer': producer, 'date_added': date_added}
    protein_filter = {
        key: {'$regex':re.compile(fr".*{value}.*", re.I)} if key == 'name' else value 
        for key in filter_keys if (value := filter_keys.get(key))
    }

    sort_props_splited = sort.split('.') 
    sort_col = sort_props_splited[0]
    sort_direction = 1 if sort_props_splited[1] == 'asc' else -1

    return {
        'results': await db["proteins"].find(protein_filter)
                                       .sort(sort_col, sort_direction)
                                       .skip((page - 1) * limit)
                                       .to_list(limit),
        'count': await db["proteins"].count_documents(protein_filter)
    }


@app.post("/proteins/", response_description="Add new record")
async def create_record(protein_data: ProteinInModel):
    protein_data = jsonable_encoder(protein_data)
    new_protein = await db["proteins"].insert_one(protein_data)
    created_protein = await db["proteins"].find_one({"_id": new_protein.inserted_id})
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, 
        content=jsonable_encoder(created_protein, custom_encoder={ObjectId: str})
    )


@app.put("/proteins/{id}/update/", response_description="Update a record", response_model=ProteinOutModel)
async def update_record(id: str, protein_data: ProteinInModel):
    protein_data = {k: v for k, v in protein_data.dict().items() if v is not None}

    if len(protein_data) >= 1:
        update_result = await db["proteins"].update_one({"_id": ObjectId(id)}, {"$set": protein_data})

        if update_result.modified_count == 1:
            if (
                updated_protein := await db["proteins"].find_one({"_id": ObjectId(id)})
            ) is not None:
                return updated_protein

    if (existing_protein := await db["proteis"].find_one({"_id": ObjectId(id)})) is not None:
        return existing_protein

    raise HTTPException(status_code=404, detail=f"Protein {id} not found")


@app.delete("/proteins/{id}/delete/", response_description="Delete a record")
async def delete_protein(id: str):
    delete_result = await db["proteins"].delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content='')

    raise HTTPException(status_code=404, detail=f"Protein {id} not found")


if __name__ == "__main__":
    uvicorn.run(app='main:app', host="127.0.0.1", port=5000, reload=True)