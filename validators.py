
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

    def select_option_from_list(self, options: list[str], qst: str) -> str:
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

        choice = self.get_valid_number(qst, int, 1, len(options))
        return options[choice - 1]
    
        
    