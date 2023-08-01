from rest_framework import serializers
from .models import Board, Column, Task, Subtask

class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = (
            'id',
            'title',
            'is_selected'
        )


class TaskListSerializer(serializers.ModelSerializer):
    subtask_count = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'subtask_count'
        )

    def get_subtask_count(self, obj):
        subtasks = obj.subtasks.prefetch_related()
        selected = subtasks.filter(is_selected=True)
        return {
            'total': subtasks.count(),
            'selected': selected.count()
        }


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True)
    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'subtasks',
            'status',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        subtasks_data = validated_data.pop('subtasks')
        task = Task.objects.create(owner=user, **validated_data)
        for subtask_data in subtasks_data:
            Subtask.objects.create(owner=user, task=task, **subtask_data)
        return task
    
    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop('subtasks')
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance    


class ColumnListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = (
            'id',
            'name'
        )


class ColumnDetailSerializer(serializers.ModelSerializer):
    tasks = TaskListSerializer(many=True, read_only=True)

    class Meta:
        model = Column
        fields = (
            'id',
            'name',
            'tasks'
        )


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = (
            'id',
            'name',
        )


class BoardDetailSerializer(serializers.ModelSerializer):
    columns = ColumnDetailSerializer(many=True)

    class Meta:
        model = Board
        fields = (
            'id',
            'name',
            'columns',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        columns_data = validated_data.pop('columns')
        board = Board.objects.create(**validated_data, owner=user)
        for column_data in columns_data:
            Column.objects.create(owner=user, board=board, **column_data)
        return board
    

    def update(self, instance, validated_data):
        columns_data = validated_data.pop('columns')
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance