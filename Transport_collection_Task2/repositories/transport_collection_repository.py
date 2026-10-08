from database import get_connection

async def get_all_collections():
    connection = await get_connection()
    try:
        async with connection.cursor() as cursor:
            await cursor.execute("""
            SELECT id,
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
            ORDER BY id
            """)
            rows = await cursor.fetchall()
            return rows
    finally:
        await connection.close()



async def get_collection_by_id(collection_id:int):
    connection = await get_connection()
    try:
        async with connection.cursor() as cursor:
            await cursor.execute("""
            SELECT id,
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
            WHERE id = %s
            """,(collection_id,))
            return await cursor.fetchone()
    finally:
        await connection.close()


async def insert_collection(data: dict):
    connection = await get_connection()
    try:
        async with connection.cursor() as cursor:

            await cursor.execute("""
                INSERT INTO transport_collections
                (
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
                )
                VALUES
                (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s
                )
                RETURNING
                    id,
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
            """, (
                data["vehicle_number"],
                data["collection_date"],
                data["driver_name"],
                data["morning_trips"],
                data["evening_trips"],
                data["morning_collection"],
                data["evening_collection"],
                data["fuel_expense"],
                data["other_expense"],
                data["total_trips"],
                data["total_collection"],
                data["total_expense"],
                data["net_collection"]
            ))

            row = await cursor.fetchone()
            await connection.commit()
            return row

    except Exception:
        await connection.rollback()
        raise

    finally:
        await connection.close()


async def update_collection( collection_id: int, data: dict):
    connection = await get_connection()
    try:
        async with connection.cursor() as cursor:
            await cursor.execute("""
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
                RETURNING
                    id,
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
            """, (
                data["vehicle_number"],
                data["collection_date"],
                data["driver_name"],
                data["morning_trips"],
                data["evening_trips"],
                data["morning_collection"],
                data["evening_collection"],
                data["fuel_expense"],
                data["other_expense"],
                data["total_trips"],
                data["total_collection"],
                data["total_expense"],
                data["net_collection"],
                collection_id
            ))

            row = await cursor.fetchone()
            if row is None:
                await connection.rollback()
                return None
            await connection.commit()
            return row

    except Exception:
        await connection.rollback()
        raise

    finally:
        await connection.close()


async def delete_collection( collection_id: int):
    connection = await get_connection()
    try:
        async with connection.cursor() as cursor:
            await cursor.execute("""
                DELETE FROM transport_collections
                WHERE id = %s
                RETURNING id
            """, (collection_id,))

            row = await cursor.fetchone()

            if row is None:
                await connection.rollback()
                return None
            
            await connection.commit()
            return row[0]

    except Exception:
        await connection.rollback()
        raise

    finally:
        await connection.close()



