import material, warehouse_management, fuel_road

def main():
    print("Witaj w programie POLMAR!")
    print("Wybierz działanie:")
    print("1. Zamowienie dla klienta")
    print("2. Magazyn")
    czy_zakonczyc = "nie"
    while czy_zakonczyc != "tak":
        option = input("Wprowadź numer opcji: ")
        if option == "1":
            material.main()
            
        elif option == "2":
            warehouse_management.main()
        czy_zakonczyc = input("Czy chcesz zakończyć? (tak/nie): ")

if __name__ == "__main__":
    main()
