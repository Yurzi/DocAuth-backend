from django.db.models import QuerySet
from rest_framework import permissions

from .models import Api, Function, Page, User


def union_permissions(
    queryset_1: list[int] | QuerySet, queryset_2: list[int] | QuerySet
) -> list[int]:
    res = set()
    for item in queryset_1:
        res.add(item)
    for item in queryset_2:
        res.add(item)

    return list(res)


def filter_permission_by_status(permissions_list: list[int] | QuerySet) -> list[int]:
    res = list()
    for permission in permissions_list:
        permission_obj = Function.objects.filter(id=permission).first()
        if permission_obj.status != Function.STATUS_CHOICES[0][0]:
            # print(permission_obj.status)
            res.append(permission)
    return res


# 获取用户对应的角色权限及其特殊权限
def get_user_permissions(user: User) -> list[int]:
    user_has_role_permissions = (
        User.objects.filter(username=user.username)
        .first()
        .roles.all()
        .values_list("role__functions__function_id", flat=True)
    )
    user_has_spec_permissions = (
        User.objects.filter(username=user.username)
        .first()
        .functions.all()
        .values_list("function_id", flat=True)
    )
    # print(user_has_spec_permissions)
    user_has_permissions = union_permissions(
        user_has_role_permissions, user_has_spec_permissions
    )
    user_has_permissions = filter_permission_by_status(user_has_permissions)
    return user_has_permissions


def check_permissions_requirements(
    user_has_permissions: list[int] | QuerySet,
    required_permissions: list[int] | QuerySet,
) -> bool:
    check_status = False
    for required in required_permissions:
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
            return check_status

    return check_status


class GeneralPermission(permissions.BasePermission):
    message = "You have not permissions to do this!"

    def has_permission(self, request, view) -> bool:
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

        if request.method in permissions.SAFE_METHODS:
            rw_type = ["r", "a"]
        else:
            rw_type = ["w", "a"]

        api_required_functions = (
            api_obj.required_functions.filter(rw_type__in=rw_type)
            .all()
            .values_list("function_id", flat=True)
        )

        # 获取用户到权限
        # print(request.user.username)
        user_has_permissions = get_user_permissions(request.user)

        # print(user_has_permissions[0])

        # 检验权限
        return check_permissions_requirements(
            user_has_permissions, api_required_functions
        )


class HasAccessOfPage(permissions.BasePermission):
    message = "You don't have the access to the page"

    def has_object_permission(self, request, view, obj: Page) -> bool:
        # 获取用户所具有的权限
        user_has_permissions = get_user_permissions(request.user)

        # 获取页面需要的权限
        page_required_functions = obj.required_functions.all().values_list(
            "function_id", flat=True
        )

        return check_permissions_requirements(
            user_has_permissions, page_required_functions
        )
