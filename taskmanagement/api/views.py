from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .permissions import IsOwner
from taskmanagement.models import (
    Board, Column,
    Task, Subtask
)
from taskmanagement.serializers import (
    BoardListSerializer, BoardDetailSerializer,
    ColumnListSerializer, TaskDetailSerializer,
    SubtaskSerializer
)


class BoardListView(APIView):
    permission_classes=(IsAuthenticated, )
    def get(self, request):
        boards = Board.objects.filter(owner=request.user)
        serializer = BoardListSerializer(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BoardCreateView(APIView):
    permission_classes=(IsAuthenticated, )
    def post(self, request):
        serializer = BoardDetailSerializer(
            data=request.data,
            context={'request':request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class BoardDetailView(APIView):
    permission_classes=(IsAuthenticated, )
    def get(self, request, pk):
        try:
            board = Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            return Response(
                {
                    'error':'Board not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        if board.owner != request.user:
            return Response(
                {
                    'error': 'You do not have permission to perform this action'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = BoardDetailSerializer(board)
        return Response(serializer.data)
    

class BoardUpdateView(APIView):
    permission_classes=(IsAuthenticated, )
    def put(self, request, pk):
        try:
            board = Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            return Response(
                {
                    'error':'Board not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        if board.owner != request.user:
            return Response(
                {
                    'error': 'You do not have permission to perform this action'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = BoardDetailSerializer(instance=board, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class BoardDeleteView(APIView):
    permission_classes=(IsAuthenticated, IsOwner)
    def delete(self, request, pk):
        try:
            board = Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            return Response(
                {
                    'error':'Board not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        if board.owner != request.user:
            return Response(
                {
                    'error': 'You do not have permission to perform this action'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ColumnListView(APIView):
    permission_classes=(IsAuthenticated, )
    def get(self, request, board_pk):
        try:
            board = Board.objects.get(pk=board_pk)
            if board.owner != request.user:
                return Response(
                    {
                        "You don`t have permission to perform this action."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
        except Board.DoesNotExist:
            return Response(
                {
                    'error':'Board not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ColumnListSerializer(board.columns.all(), many=True)
        return Response(serializer.data)


class ColumnCreateView(APIView):
    permission_classes=(IsAuthenticated, )
    def post(self, request, board_pk):
        try:
            board = Board.objects.get(pk=board_pk)
            if board.owner != request.user:
                return Response(
                    {
                        "You don`t have permission to perform this action."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
        except Board.DoesNotExist:
            return Response(
                {
                    'error':'Board not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = ColumnListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(board=board, owner=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ColumnDeleteView(APIView):
    permission_classes = (IsAuthenticated, )
    def delete(self, request, pk):
        try:
            column = Column.objects.get(pk=pk)
        except Column.DoesNotExist:
            return Response(
                {
                    'error':'Column not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        if column.owner != request.user:
            return Response(
                {
                    'error': 'You do not have permission to perform this action'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        column.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class TaskDetailView(APIView):
    permission_classes = (IsAuthenticated, IsOwner)
    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                {
                    'error': 'Task not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        if task.owner != request.user:
            return Response(
                {
                    'error': 'You do not have permission to perform this action'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data)


class TaskCreateView(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request, board_pk):
        try:
            board = Board.objects.get(pk=board_pk)
            if board.owner != request.user:
                return Response(
                    {
                        "You don`t have permission to perform this action."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            
        except Board.DoesNotExist:
            return Response(
                {
                    'error':'Board not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = TaskDetailSerializer(
            data=request.data,
            context={'request':request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class TaskUpdateView(APIView):
    permission_classes = (IsAuthenticated, )
    def put(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                {
                    'error':'Task not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        if task.owner != request.user:
            return Response(
                {
                    'error': 'You do not have permission to perform this action'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = TaskDetailSerializer(instance=task, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class TaskDeleteView(APIView):
    permission_classes = (IsAuthenticated, )
    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                {
                    'error': 'Task not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        if task.owner != request.user:
            return Response(
                {
                    'error': 'You do not have permission to perform this action'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubtaskCreateView(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request, task_pk):
        try:
            task = Task.objects.get(pk=task_pk)
            if task.owner != request.user:
                return Response(
                    {
                        "You don`t have permission to perform this action."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
        except Task.DoesNotExist:
            return Response(
                {
                    'error': 'Task not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = SubtaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task, owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {
                    'error': serializer.erorrs
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class SubtaskDeleteView(APIView):
    permission_classes = (IsAuthenticated, )
    def delete(self, request, pk):
        try:
            subtask = Subtask.objects.get(pk=pk)
        except Subtask.DoesNotExist:
            return Response(
                {
                    'error': 'Subtask not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        if subtask.owner != request.user:
            return Response(
                {
                    'error': 'You do not have permission to perform this action'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)