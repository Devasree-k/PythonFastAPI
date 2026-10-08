CREATE TABLE transport_collections (
    id SERIAL PRIMARY KEY,
    vehicle_number VARCHAR(20) NOT NULL,
    collection_date DATE NOT NULL,
    driver_name VARCHAR(100) NOT NULL,
    morning_trips INT NOT NULL,
    evening_trips INT NOT NULL,
    morning_collection NUMERIC(10,2) NOT NULL,
    evening_collection NUMERIC(10,2) NOT NULL,
    fuel_expense NUMERIC(10,2) NOT NULL,
    other_expense NUMERIC(10,2) NOT NULL,
    total_trips INT NOT NULL,
    total_collection NUMERIC(10,2) NOT NULL,
    total_expense NUMERIC(10,2) NOT NULL,
    net_collection NUMERIC(10,2) NOT NULL
);

select * from transport_collections


delete from transport_collections where id=2

INSERT INTO transport_collections(vehicle_number,collection_date,
driver_name,morning_trips,evening_trips,morning_collection,evening_collection,
fuel_expense,other_expense,total_trips,total_collection,total_expense,net_collection)
VALUES
('TN38AB1234','2026-10-07','Ramesh Kumar',5,5,7500.00,8000.00,3000.00,500.00,10,15500.00,3500.00,12000.00);
