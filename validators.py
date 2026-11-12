from datetime import datetime
class Validator:
    def __init__(self):
        pass
    
    def get_valid_number(self,prompt, cast_func, min_val=float("-inf"), max_val=float("inf"), multiple_of = None):
        while True:
            try:
                choice = cast_func(input(prompt))
                if choice < min_val or choice > max_val:
                    print(f"Niepoprawny wybór. Wprowadź numer od {min_val} do {max_val}.")
                    continue
                if multiple_of is not None and choice % multiple_of != 0:   
                    print(f"Wartość musi być podzielna przez {multiple_of}")
                    continue    
                return choice
            except ValueError:
                print(f"Niepoprawny typ danych")
            

    def select_option_from_list(self, options: list[str], qst: str) -> str:
        if not options:
            raise ValueError("Lista opcji nie może być pusta.")
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

        choice = self.get_valid_number(qst, int, 1, len(options))
        return options[choice - 1]

    def get_positive_float(self, prompt: str) -> float:
        while True:
            try:
                value = float(input(prompt))
                if value > 0:
                    return value
                else:
                    print("Wartość musi być większa od zera. Spróbuj ponownie.")
            except ValueError:
                print("Nieprawidłowa wartość. Spróbuj ponownie.")
    
    def get_valid_date(self, prompt: str) -> str:
        while True:
            date_str = input(prompt).strip()

            if not date_str:
                print("Data nie może być pusta.")
                continue

            try:
                parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                print("Nieprawidłowy format daty. Użyj formatu RRRR-MM-DD.")
                continue

            if parsed_date.date() < datetime.now().date():
                print("Data nie może być w przeszłości.")
                continue

            return parsed_date.strftime("%Y-%m-%d")