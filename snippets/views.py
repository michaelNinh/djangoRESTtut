from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import detail_route


@api_view(['GET'])
def api_root(request, format=None):
    return Response({

        'users':reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)

    })

class SnippetViewSet(viewsets.ModelViewSet):
    '''
    Automatically provide 'list', 'create', 'retrieve', 'update', 'destroy'
    
    Additionaly provide 'Highlight' action
    '''

    queryset = Snippet.objects.all() #get all snippet objects
    serializer_class = SnippetSerializer #specify serializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly) #set permissions

    #detail_route specifies custom endpoint actions
    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

