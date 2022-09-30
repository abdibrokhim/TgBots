from .models import TGClient
from .serializers import TGClientSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class TGClientList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request,):
        snippets = TGClient.objects.all()
        serializer = TGClientSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request,):
        serializer = TGClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TGClientDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return TGClient.objects.get(pk=pk)
        except TGClient.DoesNotExist:
            raise Http404

    def get(self, request, pk,):
        snippet = self.get_object(pk)
        serializer = TGClientSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk,):
        snippet = self.get_object(pk)
        serializer = TGClientSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk,):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

