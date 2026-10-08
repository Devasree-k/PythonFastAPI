from database import get_connection
from models import TransportCollectionCreate,TransportCollectionUpdate

def get_all_collections():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
            select id,
            vehicle_number,
            collection_date,
            driver_name,
            morning_trips,
            evening_trips,
            morning_collection,
            evening_collection,
            fuel_expense,
            other_expense,
            total_trips,
            total_collection,
            total_expense,
            net_collection
            FROM transport_collections
            ORDER BY id;
            """)

            rows= cursor.fetchall()
            collections = []
            for row in rows:
                collections.append({
                    "id" : row[0],
                    "vehicle_number" : row[1],
                    "collection_date" : row[2],
                    "driver_name" : row[3],
                    "morning_trips" : row[4],
                    "evening-_trips" : row[5],
                    "morning_collection": float(row[6]),
                    "evening_collection": float(row[7]),
                    "fuel_expense": float(row[8]),
                    "other_expense": float(row[9]),
                    "total_trips": row[10],
                    "total_collection": float(row[11]),
                    "total_expense": float(row[12]),
                    "net_collection": float(row[13])

                })
            return collections

    finally:
        connection.close()

        
def get_collection(collection_id:int):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
            select id,
            vehicle_number,
            collection_date,
            driver_name,
            morning_trips,
            evening_trips,
            morning_collection,
            evening_collection,
            fuel_expense,
            other_expense,
            total_trips,
            total_collection,
            total_expense,
            net_collection
            FROM transport_collections
            WHERE id=%s;""",
                (collection_id,))
            row = cursor.fetchone()

            if row is None:
                return None

            return {
                "id" : row[0],
                "vehicle_number" : row[1],
                "collection_date" : row[2],
                "driver_name" : row[3],
                "morning_trips" : row[4],
                "evening-_trips" : row[5],
                "morning_collection": float(row[6]),
                "evening_collection": float(row[7]),
                "fuel_expense": float(row[8]),
                "other_expense": float(row[9]),
                "total_trips": row[10],
                "total_collection": float(row[11]),
                "total_expense": float(row[12]),
                "net_collection": float(row[13])

            }
    finally:
        connection.close()

def create_collection(collection : TransportCollectionCreate):
    connection = get_connection()
    try:
        total_trips = (collection.morning_trips + collection.evening_trips)
        total_collections = collection.morning_collection + collection.evening_collection
        total_expense = (collection.fuel_expense +collection.other_expense)
        net_collection = (total_collections -total_expense)
        with connection.cursor() as cursor:
            cursor.execute("""
            INSERT INTO transport_collections (
                vehicle_number,
                collection_date, driver_name,
                morning_trips, evening_trips,
                morning_collection, evening_collection,
                fuel_expense,  other_expense,
                total_trips, total_collection,
                total_expense, net_collection)
                VALUES
                (%s,
                %s, %s,
                %s, %s,
                %s, %s,
                %s, %s,
                %s, %s,
                %s, %s
                )RETURNING id;""",
                (
                    collection.vehicle_number,
                    collection.collection_date,
                    collection.driver_name,
                    collection.morning_trips,
                    collection.evening_trips,
                    collection.morning_collection,
                    collection.evening_collection,
                    collection.fuel_expense,
                    collection.other_expense,
                    total_trips,
                    total_collections,
                    total_expense,
                    net_collection
                ))
            collection_id = cursor.fetchone()[0]
            connection.commit()
            return collection_id
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def delete_collection(collection_id:int):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
            DELETE FROM transport_collections WHERE id=%s
            RETURNING id;
            """,(collection_id))

            row = cursor.fetchone()
            if row is None:
                connection.rollback()
                return None
            connection.commit()
            return row[0]
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()



def update_collection( collection_id: int, collection: TransportCollectionUpdate):

    connection = get_connection()
    try:
        total_trips = (collection.morning_trips +collection.evening_trips )
        total_collection = ( collection.morning_collection +collection.evening_collection)
        total_expense = (collection.fuel_expense +collection.other_expense)
        net_collection = (total_collection -  total_expense )

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE transport_collections
                SET
                    vehicle_number = %s,
                    collection_date = %s,
                    driver_name = %s,
                    morning_trips = %s,
                    evening_trips = %s,
                    morning_collection = %s,
                    evening_collection = %s,
                    fuel_expense = %s,
                    other_expense = %s,
                    total_trips = %s,
                    total_collection = %s,
                    total_expense = %s,
                    net_collection = %s
                WHERE id = %s
                RETURNING id;
            """, (
                collection.vehicle_number,
                collection.collection_date,
                collection.driver_name,
                collection.morning_trips,
                collection.evening_trips,
                collection.morning_collection,
                collection.evening_collection,
                collection.fuel_expense,
                collection.other_expense,
                total_trips,
                total_collection,
                total_expense,
                net_collection,
                collection_id
            ))
            row = cursor.fetchone()

            if row is None:
                connection.rollback()
                return None

            connection.commit()
            return row[0]

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()






