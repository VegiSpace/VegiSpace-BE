from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser


class ApiAuthMixin:
    # permission classes
    permission_classes = (IsAuthenticated,)


class ApiAdminAuthMixin:
    permission_classes = (IsAdminUser,)


class ApiAllowAnyMixin:
    permission_classes = (AllowAny,)
