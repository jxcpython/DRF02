from rest_framework import serializers
from rest_framework import exceptions

# 每个模型需要单独定义一个序列化器
from DRF02 import settings
from api.models import Employee


class EmployeeSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    # gender = serializers.IntegerField()
    # pic = serializers.ImageField()

    # 定义models中不存在的字段  SerializerMethodField()
    # 自定义字段  返回一个盐
    salt = serializers.SerializerMethodField()

    def get_salt(self, obj):
        return "salt"

    # 自定义性别字段的返回值
    gender = serializers.SerializerMethodField()

    # self: 当前序列化器 obj：当前对象
    def get_gender(self, obj):
        print(type(obj.gender))
        # if obj.gender == 0:
        #     return "male"
        # 性别是choices类型 get_字段名_display()访问对相应的值
        return obj.get_gender_display()

    # 自定义图片返回的全路径
    pic = serializers.SerializerMethodField()

    def get_pic(self, obj):
        print(obj.pic)
        # http://127.0.0.1:8000/media/pic/1111.jpg

        return "%s%s%s" % ("http://127.0.0.1:8000", settings.MEDIA_URL, obj.pic)


class EmployeeDeSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=8,
        min_length=2,
        # 为规则自定义错误信息
        error_messages={
            "max_length": "长度太长了",
            "min_length": "长度太短了"
        }
    )
    password = serializers.CharField()
    phone = serializers.CharField(min_length=11, required=True)

    # 自定义字段  重复密码
    re_pwd = serializers.CharField()

    # TODO 在create保存对象之前  DRF提供了两个钩子函数来对数据进行校验

    # 局部钩子： 可以对反序列化中的某个字段进行校验
    # validate_想验证的字段名
    def validate_username(self, value):
        # print("1111", value, type(value))
        if "小" in value:
            raise exceptions.ValidationError("用户名有误")

        return value

    # 全局钩子  可以通过attrs获取到所有的参数
    def validate(self, attrs):
        # print("22222", attrs)
        pwd = attrs.get("password")
        re_pwd = attrs.pop("re_pwd")
        # print(attrs)
        # 自定义校验规则  两次密码不一致  则无法保存对象
        if pwd != re_pwd:
            raise exceptions.ValidationError("两次密码不一致")

        return attrs

    def create(self, validated_data):
        """
        在保存用户对象时需要重写此方法完成保存
        :param validated_data: 前端传递的需要保存的数据
        :return:
        """
        # print(validated_data)
        return Employee.objects.create(**validated_data)
