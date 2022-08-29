from rest_framework import serializers, status
from rest_framework.response import Response
from reviews.models import Review, Comment, Category, Genre, Title, TitleGenre


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        """
        checks that one reviews per title from each users
        """
        request = self.context.get("request")
        title_id = (request.parser_context['kwargs']['title_id'])
        user = request.user
        if request.method == 'POST':
            if Review.objects.filter(title=title_id, author=user).exists():
                raise serializers.ValidationError("Уже есть отзыв этого пользователя на это произведение")
        return data

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