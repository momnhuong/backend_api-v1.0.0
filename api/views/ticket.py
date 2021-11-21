from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.http.response import JsonResponse
# from api.serializers import PostSerializer, PostCreateSerializer, PostUpdateSerializer
from common.token_authentication import TokenAuthentication
from common.token_permission import TokenPermission
from rest_framework.exceptions import ParseError


@api_view(['GET', 'POST'])
def ticket_list(request):
    pass
    # if request.method == 'GET':
    #   posts = Post.objects.all().order_by('-created_at')
    #   serializer = PostSerializer(posts, many=True)
    #   response = Response(serializer.data, status=status.HTTP_200_OK)
    #   response["Access-Control-Allow-Origin"] = "*"

    #   return response

    # elif request.method == 'POST':
    #   serializer = PostSerializer(data=request.data)

    #   if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    #   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes((TokenAuthentication, ))
# @permission_classes((TokenPermission, ))
# def post_detail(request, id):

#   user_data = request.user
#   user = user_data["jit"]

#   try:
#     posts = Post.objects.get(id=id)
#   except Post.DoesNotExist:
#     return Response(status=status.HTTP_404_NOT_FOUND)

#   if request.method == 'GET':
#     serializer = PostSerializer(posts)
#     return Response(serializer.data, status=status.HTTP_200_OK)

#   elif request.method == 'PUT':
    serializer = PostUpdateSerializer(posts, data=request.data)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#   elif request.method == 'DELETE':
#     posts.delete()
#     return JsonResponse({'message': 'Post was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

#   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @authentication_classes((TokenAuthentication, ))
# @permission_classes((TokenPermission, ))
# def post_create(request, *args, **kwargs):
#   user_data = request.user
#   user = user_data["jit"]

#   request_data = request.data
#   request_data["user"] = user

#   serializer = PostCreateSerializer(data=request_data)

#   if serializer.is_valid():
#     serializer.save()
#     response = Response(serializer.data, status=status.HTTP_201_CREATED)
#     response["Access-Control-Allow-Origin"] = "*"

#     return response

#   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
