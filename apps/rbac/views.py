# @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated],
#         url_path='change-passwd', url_name='change-passwd')
# def set_password(self, request, pk=None):
#     perms = UserInfoView.get_permission_from_role(request)
#     user = User.objects.get(id=pk)
#     if 'admin' in perms or 'user_all' in perms or request.user.is_superuser:
#         new_password1 = request.data['new_password1']
#         new_password2 = request.data['new_password2']
#         if new_password1 == new_password2:
#             user.set_password(new_password2)
#             user.save()
#             return CustomResponse('密码修改成功!')
#         else:
#             return CustomResponse('新密码两次输入不一致!', status=status.HTTP_400_BAD_REQUEST)
#     else:
#         old_password = request.data['old_password']
#         if check_password(old_password, user.password):
#             new_password1 = request.data['new_password1']
#             new_password2 = request.data['new_password2']
#             if new_password1 == new_password2:
#                 user.set_password(new_password2)
#                 user.save()
#                 return CustomResponse('密码修改成功!')
#             else:
#                 return CustomResponse('新密码两次输入不一致!', status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return CustomResponse('旧密码错误!', status=status.HTTP_400_BAD_REQUEST)