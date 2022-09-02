from django.shortcuts import render, HttpResponse
from django.core import serializers
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.serializers import *
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from notes.api_v1.permissions import SuperUserReadOnly
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

from .serializers import RegisterSerializer, NotesSerializer
from notes.models import User, Notes


class RegisterUserAPIView(generics.CreateAPIView):
    """
    RegisterAPIViewSet : Create a new user with the
                        data provided by the user
    URL : /register
    METHOD : POST
    Request Data :
        {
            "email":"awais.beg@gmail.com",
            "first_name":"awais",
            "last_name":"beg",
            "username":"awaisbeg",
            "password":"awaisbeg123"
        }
    Response Data :
        {
            "id": 4,
            "email": "awais.beg@gmail.com",
            "last_login": null,
            "is_superuser": false,
            "is_staff": false,
            "is_active": true,
            "date_joined": "2022-09-02T10:09:45.054357Z",
            "first_name": "awais",
            "last_name": "beg",
            "groups": [],
            "user_permissions": []
        }
    """

    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class NotesViewSet(viewsets.ModelViewSet):
    serializer_class = NotesSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Notes.objects.all()

    def list(self, request):
        """
        list : List the notes to the user of its own
        URL : /Notes/
        METHOD : POST
        Request Data :
                request url with users Access Token
        Response Data :
            {
                "model": "notes.notes",
                "pk": 31,
                "fields": {
                    "title": "Note 6",
                    "text": "sixth-Party",
                    "date_created": "2022-09-02",
                    "date_updated": "2022-09-02",
                    "user": 4,
                    "archive": false,
                    "sharedwith": []
                }
            }
        """
        queryset = Notes.objects.all()
        user = request.user
        queryset = queryset.filter(user=user, archive=0)
        data = serializers.serialize("json", queryset)
        return HttpResponse(data, content_type="application/json")


class ArchiveViewSet(viewsets.ModelViewSet):
    queryset = Notes.objects.all()
    serializer_class = NotesSerializer
    permission_classes = [
        SuperUserReadOnly,
    ]

    def list(self, request):
        """
        list : List the Archive notes to the user
        URL : /archive?archive=True
        METHOD : POST
        Request Data :
                request url with users Access Token
        """
        queryset = Notes.objects.all()
        user = request.user
        queryset = queryset.filter(user=user, archive=1)
        data = serializers.serialize("json", queryset)
        return HttpResponse(data, content_type="application/json")

    def post(self, request, *args, **kwargs):
        """
        post : Archive the notes from the list of the notes
                written by user
        URL : /archive/{{noteid}}/
        METHOD : POST
        Request data :
            request the url with users Access token
        """
        queryset = Notes.objects.all()
        queryset = queryset.filter(pk=kwargs["pk"])
        queryset.update(archive=1)
        data = serializers.serialize("json", queryset)
        return HttpResponse(data, content_type="application/json")


@api_view(["GET", "PATCH"])
def shared(request):
    """
    shared : List out the notes which are shared with the
            current logged in user by the others
    URL : /shared
    METHOD : POST
    Request data :
        request the url with users Access token
    """
    queryset = Notes.objects.all()
    curr_user = request.user.id
    queryset = queryset.filter(sharedwith=curr_user)
    data = serializers.serialize("json", queryset)
    return HttpResponse(data, content_type="application/json")
