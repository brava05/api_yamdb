from rest_framework import serializers

from reviews.models import Review, Comment, Category, Genre, Title, TitleGenre


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('author', 'title')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('author', 'review')
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    # slug = serializers.SlugRelatedField(
    #     slug_field='slug',
    #     read_only=True
    # )
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
        # read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Title