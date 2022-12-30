from user_custom.models import User


def get_current_user_data_utils(logged_person_id):
    try:
        obj = list(
            User.objects.filter(id=logged_person_id).values('id', 'name', 'email', 'is_superuser', "is_active"))
    except:
        obj = None
    return obj


class UserDataUtils(object):

    def get_all_data_utils(self, user):
        if user.is_superuser:
            return list(User.objects.values('id', 'name', 'email'))
        else:
            return User.objects.filter(id=user.id).values("id", "name", "email")

    def get_single_one_data_utils(self, pk, user):
        try:
            if user.is_superuser:
                obj = User.objects.filter(id=pk).values('id', 'name', 'email', 'is_active', 'is_superuser')
            else:
                obj = User.objects.filter(id=user.id).values('id', 'name', 'email', 'is_active', 'is_superuser')
        except:
            obj = None
        return obj

    def get_single_new_data_utils(self, pk):
        try:
            obj = User.objects.filter(id=pk).values('id', 'name', 'email', "is_active", "is_superuser")
        except:
            obj = None
        return obj

    def create_one_data_utils(self, **data):
        obj_status = False
        try:
            a = User.objects.create(**data)
        except:
            pass
        else:
            obj_status = True
        return a.id if obj_status else obj_status

    def update_user_data_utils(self, logged_person_id, **data):
        obj = User.objects.filter(id=logged_person_id).update(**data)
        status = True if obj == 1 else False
        return status

    def delete_user_data_utils(self, pk, user):
        try:
            if user.is_superuser or int(pk) == user.id:
                obj = User.objects.get(id=pk)
                obj.delete()
                obj_status = True
        except:
            obj_status = False
        return obj_status

    def get_current_user_data_utils(self, logged_person_id):
        try:

            obj = list(
                User.objects.filter(id=logged_person_id).values('id', 'name', 'email', 'is_superuser', "is_active"))
        except:
            obj = None
        return obj