PRAGMA foreign_keys = ON;

CREATE TABLE wood_types (
    id INTEGER PRIMARY KEY,
    category TEXT NOT NULL,
    subcategory TEXT,
    wood_species TEXT,
    price_per_m3_grosze INTEGER NOT NULL
        CHECK (price_per_m3_grosze >= 0)
);

CREATE TABLE warehouse (
id INTEGER PRIMARY KEY,
wood_type_id  INTEGER NOT NULL,
m3_quantity REAL NOT NULL CHECK(m3_quantity >0),
dimensions TEXT NOT NULL,
length REAL NOT NULL CHECK(length >0),
 
 FOREIGN KEY (wood_type_id)
 REFERENCES wood_types(id)
 ON DELETE RESTRICT);

PRAGMA foreign_keys = ON;

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
