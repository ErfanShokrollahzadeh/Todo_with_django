from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializaer, UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

User = get_user_model()


# region function base view
@api_view(['GET', 'POST'])
def all_todos(request: Request):
    if request.method == 'GET':
        todos = Todo.objects.order_by('priority').all()
        serializer = TodoSerializaer(todos, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = TodoSerializaer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail_view(request: Request, todo_id: int):
    try:
        todo = Todo.objects.get(pk=todo_id)
    except Todo.DoesNotExist:
        return Response(None, status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TodoSerializaer(todo)
        return Response(serializer.data, status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = TodoSerializaer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        todo.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)


# endregion


# region class base view
class TodosListApiView(APIView):
    @extend_schema(
        request=TodoSerializaer,
        responses={201: TodoSerializaer},
        description='this api is use for get all todos list'
    )

    def get(self, request: Request):
        todos = Todo.objects.order_by('priority').all()
        serializer = TodoSerializaer(todos, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request):
        serializer = TodoSerializaer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class TodosDetailsApiView(APIView):
    def get_object(self, todo_id: int):
        try:
            todo = Todo.objects.get(pk=todo_id)
            return todo
        except Todo.DoesNotExist:
            return Response(None, status.HTTP_404_NOT_FOUND)

    def get(self, request: Request, todo_id: int):
        todo = self.get_object(todo_id)
        serializer = TodoSerializaer(todo, many=True)
        serializer = TodoSerializaer(todo)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request: Request, todo_id: int):
        todo = self.get_object(todo_id)
        serializer = TodoSerializaer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, todo_id: int):
        todo = self.get_object(todo_id)
        todo.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)


# endregion


# region mixins
class TodosListMixinApiView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializaer

    def get(self, request: Request):
        return self.list(request)

    def post(self, request: Request):
        return self.create(request)


class TodosDetailsMixinApiView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                               generics.GenericAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializaer

    def get(self, request: Request, pk):
        return self.retrieve(request)

    def put(self, request: Request, pk):
        return self.update(request)

    def delete(self, request: Request, pk):
        return self.destroy(request)


# endregion


# region generic
class TodosGenericApiViewPagination(PageNumberPagination):
    page_size = 1
    # page_size_query_param = 'page_size'
    # max_page_size = 10


class TodosListGenericApiView(generics.ListCreateAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializaer
    pagination_class = TodosGenericApiViewPagination
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]


class TodosDetailsGenericApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializaer


class TodosListGenericApiView(generics.ListCreateAPIView):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializaer


# endregion


# region viewsets
class TodosViewSetApiView(viewsets.ModelViewSet):
    queryset = Todo.objects.order_by('priority').all()
    serializer_class = TodoSerializaer
    pagination_class = LimitOffsetPagination


# endregion


# region users
class UserGenericApiView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# endregion
