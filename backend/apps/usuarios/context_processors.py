import logging

from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)


def cargo_usuario(request):
    """Context processor para adicionar o cargo do usuário ao contexto.
    
    Retorna o cargo formatado (ex: 'Diretor', 'Professor') ou 'Usuário'
    caso o usuário não esteja autenticado ou não tenha perfil.
    """
    cargo = ''
    
    if request.user.is_authenticated:
        try:
            perfil = request.user.perfil
            cargo = perfil.get_cargo_display_label()
        except ObjectDoesNotExist:
            # Usuário não tem perfil associado
            cargo = 'Usuário'
        except AttributeError:
            # request.user não tem o atributo 'perfil'
            cargo = 'Usuário'
        except Exception as e:
            # Log unexpected errors for debugging
            logger.warning(f"Erro ao obter cargo do usuário {request.user.username}: {e}")
            cargo = 'Usuário'
    
    return {'cargo_usuario': cargo}
