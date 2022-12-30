import string
import os

from datetime import timedelta
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, Group
from django.conf import settings
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import status, exceptions
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from user_custom.api.serializers import UserSerializer
from user_custom.api.utils import UserUtils
from user_custom.models import User


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class UsersApiCreateRead(ViewSet):
    # authentication_classes = ()
    data_class = UserUtils()
    permission_classes_by_action = {'create_user': [AllowAny],
                                    'get_all_user': [IsSuperUser]
                                    }

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def get_all_user(self, request):
        response = {"success": False, 'data': [],
                    "message": '!!! Ops no data found. '}
        status_code = status.HTTP_400_BAD_REQUEST
        super_user = request.user
        data = self.data_class.get_utils(super_user)
        if len(data) > 0:
            if super_user.is_superuser:
                response.update({'data': data, 'success': True})
                response.update({'message': 'data received from db '})
                status_code = status.HTTP_200_OK
            elif not super_user.is_superuser:
                response.update({'data': data, 'success': True})
                response.update({'message': 'User is not Superuser'})
                status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

    def create_user(self, request):
        password = request.data["password"]
        password1 = request.data["password1"]
        email = request.data["email"]
        qs = User.objects.filter(email=email)
        if qs.exists():
            response = {"success": False,
                        "errors": "Email Already Exists"}
            status_code = status.HTTP_406_NOT_ACCEPTABLE

        elif password == password1:
            del request.data["password1"]

            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                pk = self.data_class.create_user_utils(**request.data)
                if pk:
                    user_obj = self.data_class.get_single_new_utils(pk)
                    if user_obj:
                        response = {"success": True,
                                    "message": "The User has been created.",
                                    'data': str(pk)}
                        status_code = status.HTTP_201_CREATED
                else:
                    response = {"success": False,
                                "message": "Something Went Wrong!!!",
                                }
                    status_code = status.HTTP_400_BAD_REQUEST
            else:
                response = {"success": False,
                            "errors": serializer.errors}
                status_code = status.HTTP_406_NOT_ACCEPTABLE
        elif password != password1:
            response = {"success": False,
                        "errors": "Password Must be same"}
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        return Response(response, status=status_code)

    def edit_user(self, request, *args, **kwargs):
        logged_person_id = request.user.id
        self.object = self.get_object()
        old_password = request.data["old_password"]
        if not self.object.check_password(old_password):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
        del request.data["old_password"]
        password = request.data["password"]
        password1 = request.data["password1"]
        email = request.data["email"]
        qs = User.objects.filter(email=email).exclude(id=logged_person_id)
        if qs.exists():
            response = {"success": False,
                        "errors": "Email Already Exists"}
            status_code = status.HTTP_406_NOT_ACCEPTABLE

        elif password == password1:
            del request.data["password1"]
            User.objects.filter(id=logged_person_id).update(email=None)
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                pk = self.data_class.update_user_utils(logged_person_id, **request.data)
                response = {"success": True,
                            "message": "The User has been Updated.",
                            }
                status_code = status.HTTP_201_CREATED
            else:
                response = {"success": False,
                            "errors": serializer.errors}
                status_code = status.HTTP_406_NOT_ACCEPTABLE
        elif password != password1:
            response = {"success": False,
                        "errors": "Password Must be same"}
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        return Response(response, status=status_code)

    def specific_user(self, request, pk):
        response = {"success": False,
                    "message": ' Sorry no user has id :{}'.format(pk)}
        status_code = status.HTTP_400_BAD_REQUEST
        user_data = request.user
        user_obj = self.data_class.get_single_one_utils(pk, user_data)
        if user_obj:
            if user_data.is_superuser:
                response.update({'success': True})
                response.update({'message': 'User retrieved successfully'})
                response.update({'data': user_obj})
                status_code = status.HTTP_200_OK
            elif not user_data.is_superuser:
                response.update({'success': True})
                response.update({'message': 'User is not SuperUser, Permission Issue'})
                response.update({'data': user_obj})
                status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

    def delete_user(self, request, pk):
        response = {"success": False,
                    "message": '!!! Ops something went wrong '}
        status_code = status.HTTP_400_BAD_REQUEST
        user_data = request.user
        if not user_data.is_superuser and int(pk) != user_data.id:
            response.update({'success': False})
            response.update({'message': 'User is not Superuser , Permission Denied'})
            status_code = status.HTTP_200_OK
            return Response(response, status=status_code)
        user_status = self.data_class.delete_user_utils(pk, user_data)
        if user_status:
            response.update({'success': True})
            response.update({'message': 'User deleted successfully'})
            status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

    def get_current_user(self, request):
        response = {"success": False,
                    "message": '!!! Ops something went wrong '}
        status_code = status.HTTP_400_BAD_REQUEST
        user_obj = self.data_class.get_current_user_utils(request.user.id)
        if user_obj:
            response = {"success": True, 'data': user_obj,
                        "message": 'Login User Detail '}
            status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


