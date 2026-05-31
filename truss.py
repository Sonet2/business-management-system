import json, math
print("Obliczanie więźby dachowej")

with open("prices.json", "r", encoding="utf-8") as p:
    data = json.load(p)

def calculate_krokwie():
    krokwie_length = float(input("Podaj długość krokwi w metrach: "))
    krokwie_dimensions = input("Podaj wymiary krokwi (szerokość x wysokość) w cm: ")
    krokwie_quantity = int(input("Podaj ilość krokwi: "))
    krokwie_type = input("Podaj gatunek drewna: ")
    krokwie_spacing = float(input("Podaj rozstaw krokwi w centymetrach: "))

    krokwie_width = float(krokwie_dimensions.split("x")[0])
    krokwie_height = float(krokwie_dimensions.split("x")[1])

    krokwie_total_m3 = krokwie_length * (krokwie_width / 100) * (krokwie_height / 100) * krokwie_quantity
    krokwie_price = data["Kantówka"][krokwie_type]

    krokwie_total_price = krokwie_total_m3 * krokwie_price

    krokwie_order = {
        "Długość krokwi (m)": krokwie_length,
        "Wymiary krokwi (cm)": krokwie_dimensions,
        "Ilość krokwi": krokwie_quantity,
        "Gatunek drewna": krokwie_type,
        "Rozstaw krokwi (cm)": krokwie_spacing,
        "Całkowity metraż krokwi (m3)": math.ceil(krokwie_total_m3),
        "Całkowity koszt krokwi (zł)": math.ceil(krokwie_total_price),
    }
    return krokwie_order
def calculate_murlata():
    murlata_length = float(input("Podaj długość murlaty w metrach: "))
    murlata_dimensions = input("Podaj wymiary murlaty (szerokość x wysokość) w cm: ")
    murlata_quantity = int(input("Podaj ilość murlat: "))
    murlata_type = input("Podaj gatunek drewna: ")

    murlata_width = float(murlata_dimensions.split("x")[0])
    murlata_height = float(murlata_dimensions.split("x")[1])

    murlata_total_m3 = murlata_length * (murlata_width / 100) * (murlata_height / 100) * murlata_quantity
    
    murlata_price = data["Belka"][murlata_type]

    murlata_total_price = murlata_total_m3 * murlata_price

    murlata_order = {
        "Długość murlaty (m)": murlata_length,
        "Wymiary murlaty (cm)": murlata_dimensions,
        "Ilość murlat": murlata_quantity,
        "Gatunek drewna": murlata_type,
        "Całkowity metraż murlat (m3)": math.ceil(murlata_total_m3),
        "Całkowity koszt murlat (zł)": math.ceil(murlata_total_price),
    }
    return murlata_order

def calculate_jetka():
    jetka_length = float(input("Podaj długość jetki w metrach: "))
    jetka_dimensions = input("Podaj wymiary jetki (szerokość x wysokość) w cm: ")
    jetka_quantity = int(input("Podaj ilość jetek: "))
    jetka_type = input("Podaj gatunek drewna: ")

    jetka_width = float(jetka_dimensions.split("x")[0])
    jetka_height = float(jetka_dimensions.split("x")[1])

    jetka_total_m3 = jetka_length * (jetka_width / 100) * (jetka_height / 100) * jetka_quantity
    
    jetka_price = data["Kantówka"][jetka_type]

    jetka_total_price = jetka_total_m3 * jetka_price

    jetka_order = {
        "Długość jetki (m)": jetka_length,
        "Wymiary jetki (cm)": jetka_dimensions,
        "Ilość jetek": jetka_quantity,
        "Gatunek drewna": jetka_type,
        "Całkowity metraż jetek (m3)": math.ceil(jetka_total_m3),
        "Całkowity koszt jetek (zł)": math.ceil(jetka_total_price),
    }
    return jetka_order


def calculate_laty_kontrlaty(k=None):
    
    if k is None:
        k = calculate_krokwie()

    krokwie_length = float(k["Długość krokwi (m)"])
    krokwie_spacing = float(k["Rozstaw krokwi (cm)"])
    krokwie_quantity = int(k["Ilość krokwi"])

    kontrlaty_length = krokwie_length
    kontrlaty_dimensions = input("Podaj wymiary kontrłat (szerokość x wysokość) w cm: ")
    kontralty_quantity = krokwie_quantity

    kontrlaty_total_m3 = kontrlaty_length * (float(kontrlaty_dimensions.split("x")[0]) / 100) * (float(kontrlaty_dimensions.split("x")[1]) / 100) * kontralty_quantity
    kontralty_total_price = data["Kontrłaty"] * kontrlaty_total_m3
    

    laty_spacing = float(input("Podaj rozstaw łat w centymetrach: "))
    width_laty_arrangement = krokwie_length / (laty_spacing / 100)
    laty_length = (krokwie_spacing / 100)* (krokwie_quantity - 2)

    laty_dimensions = input("Podaj wymiary łat (szerokość x wysokość) w cm: ")  

    laty_total_m3 = laty_length * (float(laty_dimensions.split("x")[0]) / 100) * (float(laty_dimensions.split("x")[1]) / 100) * width_laty_arrangement

    laty_total_price = data["Łaty"] * laty_total_m3

    kontrlaty_laty_order = {
        "Długość kontrłat (m)": kontrlaty_length,
        "Wymiary kontrłat (cm)": kontrlaty_dimensions,
        "Ilość kontrłat": kontralty_quantity,
        "Całkowity metraż kontrłat (m3)": math.ceil(kontrlaty_total_m3),
        "Całkowity koszt kontrłat (zł)": math.ceil(kontralty_total_price),
        "Szerokość połaci (m)": math.ceil(laty_length),
        "Wymiary łat (cm)": laty_dimensions,
        "Całkowity metraż łat (m3)": math.ceil(laty_total_m3),
        "Całkowity koszt łat (zł)": math.ceil(laty_total_price),
    }
    return kontrlaty_laty_order
def calculate_platew_slupy():
    
    platew_length = float(input("Podaj długość płatew w metrach: "))
    platew_dimensions = input("Podaj wymiary płatew (szerokość x wysokość) w cm: ")
    platew_quantity = int(input("Podaj ilość płatew: "))
    platew_type = input("Podaj gatunek drewna: ")

    platew_width = float(platew_dimensions.split("x")[0])
    platew_height = float(platew_dimensions.split("x")[1])

    platew_total_m3 = platew_length * (platew_width / 100) * (platew_height / 100) * platew_quantity
    
    platew_total_price = data["Belka"][platew_type] * platew_total_m3


    slup_height = float(input("Podaj wysokość słupów w metrach: "))
    slup_dimensions = input("Podaj wymiary słupów (szerokość x głębokość) w cm: ")
    slup_quantity = int(input("Podaj ilość słupów: "))
    slup_type = input("Podaj gatunek drewna: ") 

    slup_width = float(slup_dimensions.split("x")[0])
    slup_depth = float(slup_dimensions.split("x")[1])       

    slup_total_m3 = slup_height * (slup_width / 100) * (slup_depth / 100) * slup_quantity
    
    slup__total_price = data["Belka"][slup_type] * slup_total_m3

    

    patew_slupy_order = {
        "Długość płatew (m)": platew_length,
        "Wymiary płatew (cm)": platew_dimensions,
        "Ilość płatew": platew_quantity,
        "Gatunek drewna płatew": platew_type,
        "Całkowity metraż płatew m3": math.ceil(platew_total_m3),
        "Całkowity koszt płatew (zł)": math.ceil(platew_total_price),
        "Wysokość słupów (m)": slup_height,
        "Wymiary słupów (cm)": slup_dimensions,
        "Ilość słupów": slup_quantity,
        "Gatunek drewna słupów": slup_type,
        "Całkowity metraż słupów (m3)": math.ceil(slup_total_m3),
        "Całkowity koszt słupów (zł)": math.ceil(slup__total_price),
    }
    return patew_slupy_order

def main():
    wiezba_dachowa_order = {
        "Krokwie": None,
        "Murlaty": None,
        "Jetki": None,
        "Kontrlaty i Łaty": None,
        "Płatew i Słupy": None,
        "Suma m3 zamowienia": 0,
        "Cena": 0,
    }

    while True:
        print("Wybierz pozycje z menu:")
        print("1. Dodaj krokwie")
        print("2. Dodaj jetki")
        print("3. Dodaj murlaty")
        print("4. Dodaj kontrlaty i laty")
        print("5. Dodaj płatew i słupy")
        print("6. Zakończ obliczanie wiezby dachowej")  
        choice = input("Wybierz opcję: ")
        if choice == "1":
            wiezba_dachowa_order["Krokwie"] = calculate_krokwie()
            wiezba_dachowa_order["Suma m3 zamowienia"] += wiezba_dachowa_order["Krokwie"]["Całkowity metraż krokwi (m3)"]
            wiezba_dachowa_order["Cena"] += wiezba_dachowa_order["Krokwie"]["Całkowity koszt krokwi (zł)"]
        elif choice == "2":
            wiezba_dachowa_order["Jetki"] = calculate_jetka()
            wiezba_dachowa_order["Suma m3 zamowienia"] += wiezba_dachowa_order["Jetki"]["Całkowity metraż jetek (m3)"]
            wiezba_dachowa_order["Cena"] += wiezba_dachowa_order["Jetki"]["Całkowity koszt jetek (zł)"]
        
        elif choice == "3":
            wiezba_dachowa_order["Murlaty"] = calculate_murlata()
            wiezba_dachowa_order["Suma m3 zamowienia"] += wiezba_dachowa_order["Murlaty"]["Całkowity metraż murlat (m3)"]
            wiezba_dachowa_order["Cena"] += wiezba_dachowa_order["Murlaty"]["Całkowity koszt murlat (zł)"]

        elif choice == "4":
            if wiezba_dachowa_order["Krokwie"] is not None:
                kontr = calculate_laty_kontrlaty(k=wiezba_dachowa_order["Krokwie"])
                wiezba_dachowa_order["Kontrlaty i Łaty"] = kontr
                wiezba_dachowa_order["Suma m3 zamowienia"] += kontr["Całkowity metraż kontrłat (m3)"] + kontr["Całkowity metraż łat (m3)"]
                wiezba_dachowa_order["Cena"] += kontr["Całkowity koszt kontrłat (zł)"] + kontr["Całkowity koszt łat (zł)"]
            else:
                print("Brak zapisanych krokwi — najpierw dodaj krokiew.")
        elif choice == "5":
            wiezba_dachowa_order["Płatew i Słupy"] = calculate_platew_slupy()
            wiezba_dachowa_order["Suma m3 zamowienia"] += wiezba_dachowa_order["Płatew i Słupy"]["Całkowity metraż płatew m3"]
            wiezba_dachowa_order["Cena"] += wiezba_dachowa_order["Płatew i Słupy"]["Całkowity koszt płatew (zł)"]
        elif choice == "6":
            print("Zakończono obliczanie więźby dachowej.")
            with open("truss.json", "w", encoding="utf-8") as f:
                json.dump(wiezba_dachowa_order, f, indent=4, ensure_ascii=False)
    
            print("Zamowienie poprawnie dodane do pliku truss.json")
            break
        else:
            print("Nieprawidłowy wybór.")

if __name__ == "__main__":
    main()

    

        

