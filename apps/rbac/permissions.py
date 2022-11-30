from rest_framework import permissions

from .models import Api, User, Function


def union_permissions(queryset_1, queryset_2):
    res = set()
    for item in queryset_1:
        res.add(item)
    for item in queryset_2:
        res.add(item)

    return list(res)


def filter_permission_by_status(permissions_list: list[int]):
    res = list()
    for permission in permissions_list:
        permission_obj = Function.objects.filter(id=permission).first()
        if permission_obj.status != Function.STATUS_CHOICES[0][0]:
            print(permission_obj.status)
            res.append(permission)
    return res


class GeneralPermission(permissions.BasePermission):
    message = "You have not permissions to do this!"

    def has_permission(self, request, view):
        # 检查是否已经登录
        if request.auth is None:
            return False

        # 获取访问的接口
        url = request.path

        # print(url)

        # 获取url对应到api所需要的权限
        api_obj = Api.objects.filter(path=url).first()
        if api_obj is None:
            return False

        api_required_functions = api_obj.required_functions.all().values_list("function_id", flat=True)

        # 获取用户到权限
        # print(request.user.username)

        user_has_role_permissions = User.objects.filter(username=request.user.username).first().roles.all().values_list(
            "role__functions__function_id", flat=True)
        user_has_spec_permissions = User.objects.filter(
            username=request.user.username).first().functions.all().values_list("function_id", flat=True)
        user_has_permissions = union_permissions(user_has_role_permissions, user_has_spec_permissions)
        user_has_permissions = filter_permission_by_status(user_has_permissions)

        # print(user_has_permissions[0])

        # 检车权限
        check_status = False
        for required in api_required_functions:
            if required in user_has_permissions:
                check_status = True
                continue
            # 如果没有直接找到，则查找其父权限是否存在
            while True:
                parent = Function.objects.filter(id=required).first().parent
                if parent is None:
                    check_status = False
                    break
                if parent.id in user_has_permissions:
                    check_status = True
                    break

            if not check_status:
                break

        return check_status
