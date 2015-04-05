# coding: utf-8

# django
from django.conf import settings

# third party
from easy_thumbnails.files import get_thumbnailer
from rest_framework import serializers

# own
from ..models import Volume, Series, Publisher, Person, Language


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('name', )


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('name',)


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ('id', 'name', 'url', )


class SeriesSerializer(serializers.ModelSerializer):
    original_publisher = PublisherSerializer()
    art = PersonSerializer(many=True)
    story = PersonSerializer(many=True)

    class Meta:
        model = Series
        fields = ('id', 'name', 'status', 'art', 'story', 'original_publisher')


class VolumeSerializer(serializers.ModelSerializer):
    series = SeriesSerializer()
    publisher = PublisherSerializer()
    language = LanguageSerializer()
    cover = serializers.SerializerMethodField('get_cover_thumbnail')

    def get_cover_thumbnail(self, obj):
        if obj.cover:
            path = get_thumbnailer(obj.cover).get_thumbnail({
                'size': (100, 100), 'crop': 'scale', 'autocrop': True,
            }).url
            return '{}{}'.format(settings.BASE_URL, path)
        return None

    class Meta:
        model = Volume
        fields = ('id', 'series', 'number', 'name', 'retail_price',
                  'release_date', 'publisher', 'cover', 'language')
