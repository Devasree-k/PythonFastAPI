from fastapi import (
    APIRouter,
    Path,
    Query,
    status,
    HTTPException
)



from schema.transport_collection_schema import (
    TransportCollectionCreate,
    TransportCollectionUpdate,
    TransportCollectionResponse
)
from exceptions.transport_collection_exception import TransportCollectionNotFoundException

from services.transport_collection_service import (
    get_collections,
    get_collection,
    create_collection,
    update_existing_collection,
    delete_existing_collection
)


router = APIRouter(
    prefix="/api/transport",
    tags=["Transport Collection"]
)


@router.get(
    "/",
    response_model=list[TransportCollectionResponse]
)
async def get_all():

    collections = await get_collections()

    # if vehicle_number:

    #     collections = [
    #         collection
    #         for collection in collections
    #         if collection.vehicle_number.lower()
    #         == vehicle_number.lower()
    #     ]

    return collections

@router.get(
    "/{collection_id}",
    response_model=TransportCollectionResponse
)
async def get_one(
    collection_id: int = Path(
        ...,
        gt=0
    )
):
    try:

        return await get_collection(
            collection_id
        )
    except TransportCollectionNotFoundException as e:
        raise HTTPException (
            status_code= 404,
            detail=str(e)
        )

@router.post(
    "/",
    response_model=TransportCollectionResponse,
    status_code=status.HTTP_201_CREATED
)
async def create(
    collection: TransportCollectionCreate
):

    return await create_collection(
        collection
    )

@router.put(
    "/{collection_id}",
    response_model=TransportCollectionResponse
)
async def update(
    collection_id: int = Path(
        ...,
        gt=0
    ),

    collection: TransportCollectionUpdate = None
):
    try:

        return await update_existing_collection(
            collection_id,
            collection
        )
    except TransportCollectionNotFoundException as e:
        raise HTTPException (
            status_code= 404,
            detail=str(e)
        )

@router.delete(
    "/{collection_id}"
)
async def delete(
    collection_id: int = Path(
        ...,
        gt=0
    )
):
    try:
        return await delete_existing_collection(
            collection_id
        )
    except TransportCollectionNotFoundException as e:
        raise HTTPException (
            status_code= 404,
            detail=str(e)
        )
