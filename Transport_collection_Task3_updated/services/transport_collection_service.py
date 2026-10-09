from fastapi import HTTPException
from repositories.transport_collection_repository import(
    get_all_collections,
    get_collection_by_id,
    insert_collection,
    update_collection,
    patch_collection,
    delete_collection,
    get_total_collections_count
)
from schema.transport_collection_schema import(
    TransportCollectionCreate,
    TransportCollectionUpdate,
    TransportCollectionPatch,   
    TransportCollectionResponse
)
from exceptions.transport_collection_exception import TransportCollectionNotFoundException

def row_to_collection(row):
    if row is None:
        return None

    data = {
        "id": row[0],
        "vehicle_number": row[1],
        "collection_date": row[2],
        "driver_name": row[3],
        "morning_trips": row[4],
        "evening_trips": row[5],
        "morning_collection": float(row[6]),
        "evening_collection": float(row[7]),
        "fuel_expense": float(row[8]),
        "other_expense": float(row[9]),
        "total_trips": row[10],
        "total_collection": float(row[11]),
        "total_expense": float(row[12]),
        "net_collection": float(row[13])
    }

    return TransportCollectionResponse.model_validate( data )

# async def get_collections(limit:int, offset:int):
#     rows = await get_all_collections(limit, offset)

#     return [
#         row_to_collection(row)
#         for row in rows
#     ]

async def get_collections(page :int , limit: int):
    offset = (page-1)*limit
    rows = await get_all_collections(limit, offset)
    total_records = await get_total_collections_count()
    total_pages = (total_records/limit)
    return {
        "page" : page,
        "limit" : limit,
        "total_records" : total_records,
        "total_pages": total_pages,
        "has_previous": page > 1,
        "has_next": page < total_pages,
        "data": [
            row_to_collection(row)
            for row in rows
        ] 
    }

async def get_collection( collection_id: int):
    row = await get_collection_by_id( collection_id)

    if row is None:
        raise TransportCollectionNotFoundException(collection_id)

    return row_to_collection(row)


async def create_collection(collection: TransportCollectionCreate):

    total_trips = ( collection.morning_trips + collection.evening_trips)
    total_collection = (collection.morning_collection + collection.evening_collection)
    total_expense = (collection.fuel_expense + collection.other_expense )
    net_collection = ( total_collection - total_expense )
    data = collection.model_dump()
    data["total_trips"] = total_trips
    data["total_collection"] = total_collection
    data["total_expense"] = total_expense
    data["net_collection"] = net_collection

    row = await insert_collection( data)
    return row_to_collection(row)


async def update_existing_collection( collection_id: int, collection: TransportCollectionUpdate):

    existing = await get_collection_by_id(collection_id )
    if existing is None:
        raise TransportCollectionNotFoundException(collection_id)


    total_trips = (collection.morning_trips + collection.evening_trips)
    total_collection = (collection.morning_collection + collection.evening_collection)
    total_expense = ( collection.fuel_expense + collection.other_expense)
    net_collection = ( total_collection - total_expense)
    data = collection.model_dump()
    data["total_trips"] = total_trips
    data["total_collection"] = total_collection
    data["total_expense"] = total_expense
    data["net_collection"] = net_collection


    row = await update_collection( collection_id, data)
    return row_to_collection(row)

async def patch_existing_collection( collection_id: int, collection: TransportCollectionPatch ):
    existing = await get_collection_by_id(collection_id)

    if existing is None:
        raise TransportCollectionNotFoundException(collection_id)

    data = collection.model_dump(exclude_unset=True)

    if not data:
        raise  HTTPException(
            status_code=400,
            detail="At least one field must be provided for PATCH"
        )

    updated_data = {
        "vehicle_number": data.get("vehicle_number", existing[1]),
        "collection_date": data.get("collection_date", existing[2]),
        "driver_name": data.get("driver_name", existing[3]),
        "morning_trips": data.get("morning_trips", existing[4]),
        "evening_trips": data.get("evening_trips", existing[5]),
        "morning_collection": float( data.get("morning_collection", existing[6] ) ),
        "evening_collection": float( data.get( "evening_collection", existing[7]) ) ,
        "fuel_expense": float(data.get( "fuel_expense", existing[8])),
        "other_expense": float(data.get( "other_expense", existing[9]))
    }

    updated_data["total_trips"] = ( updated_data["morning_trips"] + updated_data["evening_trips"] )

    updated_data["total_collection"] = (updated_data["morning_collection"] + updated_data["evening_collection"] )

    updated_data["total_expense"] = ( updated_data["fuel_expense"] + updated_data["other_expense"] )

    updated_data["net_collection"] = ( updated_data["total_collection"] - updated_data["total_expense"] )

    row = await patch_collection( collection_id, updated_data)

    return row_to_collection(row)

async def delete_existing_collection( collection_id: int):

    existing = await get_collection_by_id( collection_id )

    if existing is None:
        raise TransportCollectionNotFoundException(collection_id)


    deleted_id = await delete_collection( collection_id)

    return {
        "message": "Transport collection deleted successfully",
        "collection_id": deleted_id
    }

