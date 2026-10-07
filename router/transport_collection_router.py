from fastapi import APIRouter , HTTPException
from models import TransportCollectionUpdate, TransportCollectionCreate

from repository.transport_collection_crud import (get_all_collections,
                                                  get_collection,
                                                  create_collection,
                                                  delete_collection,
                                                  update_collection)

router = APIRouter(
    prefix = "/api/transport", 
    tags=["Transport Collection"]
)

@router.get("/")
def get_collections():
    return get_all_collections()


@router.get("/{collection_id}")
def get_collection_by_id(collection_id:int):
    collection = get_collection(collection_id)
    if collection is None:
        raise HTTPException(
            status_code = 404,
            detail="Transport collection not found."
        )
    return collection

@router.post("/")
def create_new_collection(collection :TransportCollectionCreate):
    try:
        collection_id = create_collection(collection)
        return {
            "message" : "Transport collection created successfully",
            "collection_id":collection_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Server exception {e}")

@router.delete("/{collection_id}")
def delete_from_collection(collection_id:int):
    delete_id = delete_collection(collection_id)
    if delete_id is None:
        raise HTTPException(status_code=404, detail="Transport collection not found")

    return {
        "message" : "Transport collection deleted successfully",
        "collection_id" : delete_id
    }

@router.put("/{collection_id}")
def update_existing_collection(collection_id: int, collection: TransportCollectionUpdate):

    updated_id = update_collection( collection_id, collection)

    if updated_id is None:
        raise HTTPException(
            status_code=404,
            detail="Transport collection not found"
        )

    return {
        "message": "Transport collection updated successfully",
        "collection_id": updated_id
    }



