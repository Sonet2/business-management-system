from database import Database 

class Customers:
    def __init__(self, connection):
        self.connection = connection

    def _fetch_flat_list(self, query, params=()):
                rows = self.connection.execute(query,params).fetchall()
                return[row[0] for row in rows]

    def add_customers(self, customer_type, first_name, last_name, company_name, nip, phone, email):
        if customer_type == "PERSON":
            result = self.connection.execute("""
            INSERT INTO customers (customer_type, first_name, last_name, phone, email)
            VALUES ('PERSON', ?, ?, ?, ?)""", (first_name, last_name, phone, email))
        elif customer_type == "COMPANY":
            result = self.connection.execute("""
            INSERT INTO customers (customer_type, company_name, nip, phone, email)
            VALUES ('COMPANY', ?, ?, ?, ?)""", (company_name, nip, phone, email))

        self.connection.commit()
        if result.rowcount > 0:
            print("Klient został poprawnie dodany do bazy danych")
        else:
             raise Exception("Nie udało się dodać klienta do bazy danych")
    def delete_customers(self, id_to_delete: int):
        result = self.connection.execute("DELETE FROM customers WHERE id = ?", (id_to_delete,))
        self.connection.commit()

        if result.rowcount > 0:
            return True
        return False

    def display_customers(self):
        results = self.connection.execute("SELECT * FROM customers").fetchall()
        for entry in results:
            if entry[1] == "PERSON":
                print(f"ID: {entry[0]}, Typ klienta: {entry[1]}, Imię: {entry[2]}, Nazwisko: {entry[3]}, Telefon: {entry[4]}, Email: {entry[5]}")
            elif entry[1] == "COMPANY":
                print(f"ID: {entry[0]}, Typ klienta: {entry[1]}, Nazwa firmy: {entry[6]}, NIP: {entry[7]}, Telefon: {entry[4]}, Email: {entry[5]}")

class CustomerManager:
    def __init__(self, validator, customers):
        self.validator = validator
        self.customers = customers
    def add_customer(self):
        types = ["PERSON", "COMPANY"]
        customer_type = self.validator.select_option_from_list(types, "Wybierz typ klienta: ")
        

        if customer_type == "PERSON":
            first_name = input("Podaj imię klienta: ")
            last_name = input("Podaj nazwisko klienta: ")
            phone = input("Podaj numer telefonu klienta: ")
            email = input("Podaj adres email klienta: ")
            self.customers.add_customers(customer_type, first_name, last_name, None, None, phone, email)
        elif customer_type == "COMPANY":
            company_name = input("Podaj nazwę firmy: ")
            nip = input("Podaj NIP firmy: ")
            phone = input("Podaj numer telefonu firmy: ")
            email = input("Podaj adres email firmy: ")
            self.customers.add_customers(customer_type, None, None, company_name, nip, phone, email)

    def delete_customer(self):
        self.customers.display_customers()
        id_to_delete = self.validator.get_valid_number("Podaj ID klienta do usunięcia: ", int)
        if self.customers.delete_customers(id_to_delete):
            print(f"Klient o ID {id_to_delete} został usunięty.")
        else:
            print(f"Nie znaleziono klienta o ID {id_to_delete}.")

class DeliveryLocations:
    def __init__(self, connection):
        self.connection = connection

    def _fetch_flat_list(self, query, params=()):
        rows = self.connection.execute(query,params).fetchall()
        return[row[0] for row in rows]

    def get_customer_name(self):
        results = self.connection.execute("""
        SELECT customer.id, customers.type, customers.name, customers.last_name, customers.company_name FROM customers """).fetchall()
        customers = []
        for entry in results:
            if entry[1] == "PERSON":
                description = (f"Id:{entry[0]} Imie:{entry[2]} Nazwisko:{entry[3]}")
            elif entry[1] == "COMPANY":
                description = (f"Id:{entry[0]} Nazwa firmy:{entry[4]}")
            customers.append((entry[0], description))
        return customers

    def add_delivery_locations(self, customer_id, name, address):
        result =self.connection.execute("""
            INSERT INTO delivery_locations (customer_id, name, address)
            VALUES (?, ?, ?)""", (customer_id, name, address))
        self.connection.commit()

        if result.rowcount > 0:
            print("Miejsce dostawy zostało poprawnie dodane do bazy danych")
        else:
            raise Exception("Nie udało się dodać miejsca dostawy do bazy danych")

    def delete_delivery_locations(self, id_to_delete: int):
        result = self.connection.execute("DELETE FROM delivery_locations WHERE id = ?", (id_to_delete,))
        self.connection.commit()

        if result.rowcount > 0:
            return True
        return False

    def display_delivery_locations(self):
        results = self.connection.execute("""
        SELECT delivery_locations.id, customers.first_name, customers.last_name, customers.company_name, delivery_locations.name, delivery_locations.address
        FROM delivery_locations INNER JOIN customers ON delivery_locations.customer_id = customers.id
        """)

        for entry in results:
            if entry[1] is not None and entry[2] is not None:
                print(f"ID: {entry[0]}, Klient: {entry[1]} {entry[2]}, Nazwa miejsca dostawy: {entry[4]}, Adres: {entry[5]}")
            elif entry[3] is not None:
                print(f"ID: {entry[0]}, Klient: {entry[3]}, Nazwa miejsca dostawy: {entry[4]}, Adres: {entry[5]}")
class DeliveryLocationManager:
    def __init__(self, validator, delivery_locations):
        self.validator = validator
        self.delivery_locations = delivery_locations

    def add_delivery_location(self):
        customer_ids_list = self.delivery_locations.get_customer_name()
        if not customer_ids_list:
            print("Brak klientów w bazie danych. Najpierw dodaj klienta.")
            return
        customer_id_list_int = []
        for index, customer in enumerate(customer_ids_list):
            customer_id_list_int.append(index + 1)

        customer_id = self.validator.select_option_from_list(customer_id_list_int, "Wybierz klienta (ID): ")
        name = input("Podaj nazwę miejsca dostawy: ")
        address = input("Podaj adres miejsca dostawy: ")
        self.delivery_locations.add_delivery_location(customer_id, name, address)

    def delete_delivery_location(self):
        self.delivery_locations.display_delivery_locations()
        id_to_delete = self.validator.get_valid_number("Podaj ID miejsca dostawy do usunięcia: ", int)
        if self.delivery_locations.delete_delivery_locations(id_to_delete):
            print(f"Miejsce dostawy o ID {id_to_delete} zostało usunięte.")
        else:
            print(f"Nie znaleziono miejsca dostawy o ID {id_to_delete}.")

    

        


        

    
     