CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    customer_type TEXT NOT NULL
        CHECK (customer_type IN ('PERSON', 'COMPANY')),
    first_name TEXT,
    last_name TEXT,
    company_name TEXT,
    nip TEXT UNIQUE,
    phone TEXT,
    email TEXT
);
CREATE TABLE delivery_locations (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    address TEXT NOT NULL,

    FOREIGN KEY (customer_id)
        REFERENCES customers(id)
        ON DELETE RESTRICT
);
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
CREATE TABLE orders(
id INTEGER NOT NULL PRIMARY KEY ,
customer_id INTEGER NOT NULL,
delivery_location_id INTEGER NOT NULL,
order_type TEXT NOT NULL CHECK (order_type IN ('TRUSS', 'LOOSE')),
total_order_price_grosze INTEGER NOT NULL DEFAULT 0
CHECK (total_order_price_grosze >= 0),
total_m3 REAL NOT NULL DEFAULT 0 CHECK (total_m3  >= 0),
FOREIGN KEY (customer_id) REFERENCES customers(id),
FOREIGN KEY (delivery_location_id) REFERENCES delivery_locations(id));
CREATE TABLE order_items(
id INTEGER NOT NULL PRIMARY KEY ,
order_id INTEGER NOT NULL,
material_id INTEGER NOT NULL,
m3_quantity REAL NOT NULL CHECK (m3_quantity > 0),
length REAL NOT NULL CHECK (length > 0),
dimensions TEXT NOT NULL,
line_total_grosze INTEGER NOT NULL 
CHECK (line_total_grosze >= 0),
FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
FOREIGN KEY (material_id) REFERENCES materials(id) ON DELETE RESTRICT
);
