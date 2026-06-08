from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from .models import CustomUser
from holics.models import animes


def user_gains_perms(user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    # any permission check will cache the current set of permissions
    user.has_perm("holics.add_animes")

    content_type = ContentType.objects.get_for_model(animes)
    permission = Permission.objects.get(
        codename="change_animes",
        content_type=content_type,
    )
    user.user_permissions.add(permission)

    # Checking the cached permission set
    user.has_perm("holics.add_animes")  # False