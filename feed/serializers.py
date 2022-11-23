from rest_framework import serializers

from .models import Category, Feed, Source, CategoryName


class SourceSerializer(serializers.PrimaryKeyRelatedField,
                       serializers.ModelSerializer):

    class Meta:
        model = Source


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    source = SourceSerializer(many=True,
                              queryset=Source.objects.all(),
                              required=True)

    class Meta:
        model = Category
        fields = ('name', 'source')

    def create(self, validated_data):
        sources = validated_data.pop('source')
        if not sources:
            raise serializers.ValidationError('No sources provided')

        categoryName = CategoryName.objects.get_or_create(
            name=validated_data['name'])[0]
        category, created = Category.objects.get_or_create(
            user = self.context['request'].user,
            name = categoryName,
        )
        category.source.set(sources)
        return category


class FeedSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField(read_only=True)
    bookmarked = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Feed
        fields = ('author', 'title', 'link', 'published', 'updated',
                  'categories', 'bookmarked')

    def get_categories(self, obj):
        return obj.categories.values_list('name__name', flat=True)

    def get_bookmarked(self, obj):
        return obj.bookmarks.filter(
            user=self.context['request'].user.id).exists()
