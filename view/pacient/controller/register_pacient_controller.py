class RegisterPacientController:
    def __init__(self, register_pacient_callback):
        self.register_pacient_callback = register_pacient_callback
        
def validate_fields(
    self,
    name: str,
    age: int,
    sleep_hours: int,
) -> bool:
    if (not name or len(name) < 3 or len(name) > 50):
        self.show_error("Nome deve ter entre 3 e 50 caracteres.")
        return False
    if (age < 1 or age > 150):
        self.show_error("Idade inválida.")
        return False
    if (sleep_hours < 0 or sleep_hours > 24):
        self.show_error("Horas de sono inválidas.")
        return False
