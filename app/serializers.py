from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework import exceptions

from app.models import Book, Press


# class BookSerializers(Serializer):
#     book_name= serializers.CharField()
#     price =serializers.CharField()


class BookModelSerializer(ModelSerializer):
    class Meta:
        model = Book
        # fields = ("book_name", "price", "pic")
        # fields="__all__"
        exclude = ("is_delete", "status", "id")

        # 指定查询的深度
        # depth = 1


class BookModelDeSerializer(ModelSerializer):
    """
    图书的反序列化
    """

    class Meta:
        model = Book
        fields = ("book_name", "price", "publish", "authors")
        # 为反序列化添加验证规则
        extra_kwargs = {
            "book_name": {
                "max_length": 18,  # 设置当前字段的最大长度
                "min_length": 2,
                "error_messages": {
                    "max_length": "长度太长了",
                    "min_length": "长度太短了",
                }
            },
            "price": {
                "required": True,
                "decimal_places": 2,
            }
        }

    # 全局钩子同样适用于 ModelSerializer
    def validate(self, attrs):
        name = attrs.get("book_name")
        book = Book.objects.filter(book_name=name)
        if len(book) > 0:
            raise exceptions.ValidationError('图书名已存在')

        return attrs

    # 局部钩子的使用  验证每个字段
    def validate_price(self, obj):
        print(type(obj), "1111")
        # 价格不能超过1000
        if obj > 1000:
            raise exceptions.ValidationError("价格最多不能超过1000")
        return obj


class BookModelSerializerV2(ModelSerializer):
    """
    序列化器与反序列化器整合
    """

    class Meta:
        model = Book
        fields = ("book_name", "price", "pic", "publish", "authors")

        # 添加DRF的校验规则
        extra_kwargs = {
            "book_name": {
                "max_length": 18,
                "min_length": 2,
            },
            # 只参与反序列化
            "publish": {
                "write_only": True,
            },
            "authors": {
                "write_only": True,
            },
            # 只参与序列化
            "pic": {
                "read_only": True
            }
        }

    # 全局钩子
    def validate(self, attrs):
        name = attrs.get("book_name")
        book = Book.objects.filter(book_name=name)
        if len(book) > 0:
            raise exceptions.ValidationError('图书名已存在')

        return attrs

    # 局部钩子
    def validate_price(self, obj):
        if obj > 1000:
            raise exceptions.ValidationError("价格最多不能超过10000")
        return obj

    # 重写update方法完成更新
    def update(self, instance, validated_data):
        print(instance, "11111")
        print(validated_data)
        book_name = validated_data.get("book_name")
        instance.book_name = book_name
        instance.save()
        return instance

