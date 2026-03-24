from rest_framework import permissions

class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Custom Permission:
    - User Publik (Anonim): Boleh melihat data (GET).
    - User Staff (Admin): Boleh mengubah data (POST, PUT, DELETE).
    """

    def has_permission(self, request, view):
        # 1. Izinkan metode 'aman' (GET, HEAD, OPTIONS) untuk siapa saja
        if request.method in permissions.SAFE_METHODS:
            return True

        # 2. Metode tulis (POST, DELETE, PUT) hanya untuk user yang login DAN berstatus staff
        return request.user and request.user.is_staff