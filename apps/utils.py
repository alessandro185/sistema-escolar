# Utilidades para o projeto

def formatar_cpf(cpf):
    """Formata CPF para o padrão XXX.XXX.XXX-XX"""
    if not cpf:
        return ""
    cpf = cpf.replace(".", "").replace("-", "")
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def limpar_cpf(cpf):
    """Remove formatação do CPF"""
    return cpf.replace(".", "").replace("-", "")


def formatar_telefone(telefone):
    """Formata telefone para o padrão (XX) XXXXX-XXXX"""
    if not telefone:
        return ""
    telefone = telefone.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
    
    if len(telefone) == 11:
        return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
    elif len(telefone) == 10:
        return f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"
    
    return telefone


def calcular_idade(data_nascimento):
    """Calcula a idade baseada na data de nascimento"""
    from datetime import date
    today = date.today()
    return today.year - data_nascimento.year - (
        (today.month, today.day) < (data_nascimento.month, data_nascimento.day)
    )
