from users.models import User


def user_has_any_role(user_id: int, *role_names) -> bool:
    try:
        user_role = User.objects.filter(
            id=user_id,
            deleted_at=None
        ).select_related('role').values_list('role__name', flat=True).first()

        if not user_role:
            return False

        valid_roles = [r.upper() for r in role_names]
        return user_role.upper() in valid_roles

    except Exception:
        return False