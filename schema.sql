CREATE TABLE wood_species (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE materials (
    id INTEGER PRIMARY KEY,
    category TEXT NOT NULL,
    subcategory TEXT,
    wood_species_id INTEGER,
    price_per_m3_grosze INTEGER NOT NULL
        CHECK (price_per_m3_grosze >= 0),
		
		FOREIGN KEY (wood_species_id)
		REFERENCES wood_species(id)
		ON DELETE RESTRICT
);
CREATE TABLE warehouse (
id INTEGER PRIMARY KEY,
material_id  INTEGER NOT NULL,
m3_quantity REAL NOT NULL CHECK(m3_quantity >0),
dimensions TEXT NOT NULL,
length REAL NOT NULL CHECK(length >0),
 
 FOREIGN KEY (material_id)
 REFERENCES materials(id)
 ON DELETE RESTRICT);
CREATE TABLE delivery_locations (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    name TEXT,
    address TEXT, distance REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);
CREATE TABLE "order_items" (
	"id"	INTEGER NOT NULL,
	"order_id"	INTEGER NOT NULL,
	"material_id"	INTEGER NOT NULL,
	"m3_quantity"	REAL NOT NULL CHECK("m3_quantity" > 0),
	"length"	REAL NOT NULL CHECK("length" > 0),
	"dimensions"	TEXT NOT NULL,
	"price_per_m3_grosze"	INTEGER NOT NULL,
	"line_total_grosze"	INTEGER NOT NULL CHECK("line_total_grosze" >= 0),
	PRIMARY KEY("id"),
	FOREIGN KEY("material_id") REFERENCES "materials"("id") ON DELETE RESTRICT,
	FOREIGN KEY("order_id") REFERENCES "orders"("id") ON DELETE CASCADE
);
CREATE TRIGGER calculate_line_total_insert
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    UPDATE order_items
    SET line_total_grosze = CAST(
        ROUND(NEW.price_per_m3_grosze * NEW.m3_quantity)
        AS INTEGER
    )
    WHERE id = NEW.id;
END;
CREATE TRIGGER calculate_line_total_update
AFTER UPDATE OF price_per_m3_grosze, m3_quantity
ON order_items
FOR EACH ROW
BEGIN
    UPDATE order_items
    SET line_total_grosze = CAST(
        ROUND(NEW.price_per_m3_grosze * NEW.m3_quantity)
        AS INTEGER
    )
    WHERE id = NEW.id;
END;
CREATE TRIGGER update_order_totals
AFTER UPDATE OF line_total_grosze ON order_items
FOR EACH ROW
BEGIN
UPDATE orders
SET total_order_price_grosze = COALESCE((
SELECT SUM(order_items.line_total_grosze)
FROM order_items
WHERE order_items.order_id = NEW.order_id
), 0) + COALESCE(fuel_cost_grosze, 0)
WHERE orders.id = NEW.order_id;

UPDATE orders
SET total_m3 = COALESCE((
SELECT SUM(order_items.m3_quantity)
FROM order_items
WHERE order_items.order_id = NEW.order_id),0)
WHERE orders.id = NEW.order_id;

END;
CREATE TRIGGER update_order_totals_after_delete
AFTER DELETE ON  order_items
FOR EACH ROW
BEGIN
UPDATE orders
SET total_order_price_grosze = COALESCE((
SELECT SUM(order_items.line_total_grosze)
FROM order_items
WHERE order_items.order_id = OLD.order_id
), 0) + COALESCE(fuel_cost_grosze, 0)
WHERE orders.id = OLD.order_id;

UPDATE orders
SET total_m3 = COALESCE((
SELECT SUM(order_items.m3_quantity)
FROM order_items
WHERE order_items.order_id = OLD.order_id),0)
WHERE orders.id = OLD.order_id;

END;
CREATE TABLE "orders" (
"id"	INTEGER NOT NULL,
"customer_id"	INTEGER NOT NULL,
"delivery_location_id"	INTEGER NOT NULL,
"order_type"	TEXT NOT NULL CHECK("order_type" IN ('TRUSS', 'LOOSE')),
"total_order_price_grosze"	INTEGER NOT NULL DEFAULT 0 CHECK("total_order_price_grosze" >= 0),
"total_m3"	REAL NOT NULL DEFAULT 0 CHECK("total_m3" >= 0),
"status"	TEXT NOT NULL DEFAULT 'IN_PROGRESS' CHECK("status" IN ('IN_PROGRESS', 'COMPLETED', 'CANCELLED')),
"created_at"	TEXT NOT NULL,
"delivery_date"	TEXT,
"fuel_cost_grosze"	INTEGER,
"fuel_consumption"	REAL,
PRIMARY KEY("id"),
FOREIGN KEY("customer_id") REFERENCES "customers"("id"),
FOREIGN KEY("delivery_location_id") REFERENCES "delivery_locations"("id")
);
CREATE TRIGGER update_fuel_cost
AFTER UPDATE OF fuel_cost_grosze ON orders
FOR EACH ROW
BEGIN
UPDATE orders
SET total_order_price_grosze = COALESCE((
SELECT SUM(order_items.line_total_grosze)
FROM order_items
WHERE order_items.order_id = NEW.id
), 0) + COALESCE(fuel_cost_grosze, 0)
WHERE orders.id = NEW.id;
END;
CREATE TABLE "customers" (
    id INTEGER PRIMARY KEY,
    customer_type TEXT NOT NULL
        CHECK (customer_type IN ('PERSON', 'COMPANY')),
    first_name TEXT,
    last_name TEXT,
    company_name TEXT,
    nip TEXT UNIQUE,
    phone TEXT,
    email TEXT,
	
	CHECK (
    CASE
        WHEN customer_type = 'PERSON' THEN
            first_name IS NOT NULL
            AND length(trim(first_name)) > 0
            AND last_name IS NOT NULL
            AND length(trim(last_name)) > 0
            AND company_name IS NULL
            AND nip IS NULL

        WHEN customer_type = 'COMPANY' THEN
            company_name IS NOT NULL
            AND length(trim(company_name)) > 0
            AND nip IS NOT NULL
            AND length(trim(nip)) > 0
            AND first_name IS NULL
            AND last_name IS NULL

        ELSE 0
    END
)
	
	
);
