import random
import string
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
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


def generate_verification_code(length=6):
    """Generate a random verification code with letters and numbers"""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def send_password_reset_email(user, verify_code):
    """Send password reset email with verification code"""
    try:
        subject = 'Recuperación de Contraseña - CanEduca'
        
        # Render HTML template
        html_message = render_to_string('emails/password_reset.html', {
            'user': user,
            'verify_code': verify_code
        })
        
        # Send email
        send_mail(
            subject=subject,
            message=f'Tu código de verificación es: {verify_code}',  # Plain text fallback
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False