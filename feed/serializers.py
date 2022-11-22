from rest_framework import serializers

from .models import Category, Feed, Source


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
        category, created = Category.objects.get_or_create(**validated_data)
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
        return obj.categories.values_list('name', flat=True)

    def get_bookmarked(self, obj):
        return obj.bookmarks.filter(
            user=self.context['request'].user.id).exists()
