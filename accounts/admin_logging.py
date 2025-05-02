# core/admin_logging.py
from functools import wraps
import logging

from crum import get_current_user
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()

def _get_system_user_pk() -> str | None:
    """
    Повертає PK першого superuser (якщо він є),
    або None — тоді LogEntry пропускається.
    """
    return User.objects.filter(is_superuser=True).values_list("pk", flat=True).first()

def admin_log(msg: str, *, flag=ADDITION):
    """
    Декоратор: записує LogEntry, гарантуючи дійсний user_id (не None).
    Якщо користувача немає — тихо пропускає запис.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(sender, instance, *args, **kwargs):
            result = func(sender, instance, *args, **kwargs)

            user = get_current_user()
            if user and user.is_authenticated:
                uid = user.pk
            else:
                uid = _get_system_user_pk()      # ← UUID реального superuser-а

            if uid is None:                     # усе ще нікого — просто пропустимо
                logger.warning("LogEntry пропущено: немає valid user_id")
                return result

            try:
                LogEntry.objects.log_action(
                    user_id=uid,
                    content_type_id=ContentType.objects.get_for_model(instance).pk,
                    object_id=instance.pk,
                    object_repr=str(instance)[:200],
                    action_flag=flag,
                    change_message=msg.format(instance=instance, result=result),
                )
            except Exception:
                logger.exception("Не вдалося створити LogEntry")

            return result
        return wrapper
    return decorator
