# articles/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Article, Comment
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer

# 게시글 목록 조회 및 생성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list_create(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

# 게시글 상세조회, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def article_detail_update_delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        if request.user == article.user:
            serializer = ArticleSerializer(article, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    elif request.method == 'DELETE':
        if request.user == article.user:
            article.delete()
            return Response({'detail': '게시글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

# 댓글 생성 및 삭제
@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_create_delete(request, article_pk, comment_pk=None):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        if comment_pk:
            comment = get_object_or_404(Comment, pk=comment_pk)
            if request.user == comment.user:
                comment.delete()
                return Response({'detail': '댓글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

# 댓글 수정
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def comment_update(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    if request.user != comment.user:
        return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = CommentSerializer(comment, data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)