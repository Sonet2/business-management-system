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
