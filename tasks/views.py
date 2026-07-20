from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination

from .serializers import TaskSerializer
from .models import Task


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks(request):
    user = request.user

    tasks = Task.objects.filter(user_id=user.id).order_by("-date_created")

    paginator = PageNumberPagination()
    paginator.page_size = 8

    result_data = paginator.paginate_queryset(tasks, request)

    serializer = TaskSerializer(result_data, many=True)

    return paginator.get_paginated_response(serializer.data)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_tasks(request):
    user = request.user
    serializer = TaskSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    task = user.tasks.create(**serializer.validated_data)

    instance = TaskSerializer(task)

    return Response(instance.data, status=status.HTTP_200_OK)    


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request):
    try:
        task_id = request.data['task_action']
        if task_id == 'all':
            user = request.user
            task = Task.objects.filter(user_id=user.id).delete()
        else:
            user = request.user
            task = get_object_or_404(Task, id=task_id, user_id=user.id)
            task.delete()
    except KeyError as e:
        return Response({
            'error': 'You most write the key or the correct key to delete'
        }, status=status.HTTP_400_BAD_REQUEST)

        
    return Response({
        'message': 'Successful operation'
    }, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request):
    task_id = request.data['task_id']
    task = get_object_or_404(Task, id=task_id)

    serializer = TaskSerializer(instance=task, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)

    serializer.save()
    
    return Response({
        "message": "Successfully updated",
        "task": serializer.data
    }, status=status.HTTP_200_OK)