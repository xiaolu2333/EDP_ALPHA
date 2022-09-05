# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView
#
#
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     """ 自定义 TokenObtainPairSerializer 类，添加自定义字段 """
#     # def update(self, instance, validated_data):
#     #     pass
#     #
#     # def create(self, validated_data):
#     #     pass
#
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#
#         # Add custom claims
#         token['username'] = user.username
#         token['role'] = user.role
#         token['status'] = user.status
#
#         return token
#
#
# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer
