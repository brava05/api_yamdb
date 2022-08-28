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
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='name', read_only=False,
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        many=False,
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        required=False,
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False, read_only=True),
    genre = GenreSerializer(many=True, required=False, read_only=True),
    rating = serializers.IntegerField()

    class Meta:
        fields = (
            'id', 'name', 'description', 'year',
            'category', 'genre', 'rating'
        )
        model = Title
