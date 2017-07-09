from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    '''
    custom permission to only allow owners of snip to edit
    '''

    def has_object_permission(self, request, view, obj):

        # read permissions only
        if request.method in permissions.SAFE_METHODS:
            return True

        # write permission only for owner of post
        return obj.owner == request.user