# from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN


def is_owner(obj, request):
    if obj.owner != request.user:
        return Response(
            {
                'error': 'You do not have permission to perform this action'
            },
            status=HTTP_403_FORBIDDEN
        )


# class IsOwner(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj and obj.owner == request.user