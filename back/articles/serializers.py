# articles/serializers.py
from rest_framework import serializers
from .models import Article, Comment

# 댓글
class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = (
            'id',
            'content',
            'username',
            'created_at',
        )
# 글, 목록용
class ArticleListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    
    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'username',
            'comment_count',
            'created_at',
        )
# 글, 상세정보용
class ArticleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'content',
            'username',
            'comments',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('user',)