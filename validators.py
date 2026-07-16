
class Validator:
    def __init__(self):
        pass
    
    def get_valid_number(self,prompt, cast_func, min_val=float("-inf"), max_val=float("inf")):
        while True:
            try:
                choice = cast_func(input(prompt))
                if min_val <= choice <= max_val:
                    return choice
                else:
                    print(f"Niepoprawny wybór. Wprowadź numer od {min_val} do {max_val}.")
            except ValueError:
                print(f"Niepoprawny typ danych")

    
    
        
    