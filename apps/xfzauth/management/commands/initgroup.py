from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group,Permission,ContentType
from apps.news.models import News,NewsCategory,Banner


class Command(BaseCommand):
    def handle(self, *args, **options):
        # 1.编辑组(管理文章/管理课程/管理轮播图)
        # 这步找到所有的权限类型
        edit_content_types = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(NewsCategory),
            ContentType.objects.get_for_model(Banner),
        ]
        # 由这个找到这些类型的所有权限
        edit_permissions = Permission.objects.filter(
            content_type__in=edit_content_types)
        # 创建分组,并把权限添加给分组中
        editGroup = Group.objects.create(name='编辑2')
        editGroup.permissions.set(edit_permissions)
        editGroup.save()
        self.stdout.write(self.style.SUCCESS('编辑分组创建完成'))
        # 2.财务组(这个由于课程那部分没写，先在这里定义完了再说)
        # 这个就不用写了，没实现它的功能

        # 3.管理员组
        admin_permissions = edit_permissions.union()
        adminGroup = Group.objects.create(name='管理员')
        adminGroup.permissions.set(admin_permissions)
        adminGroup.save()
        self.stdout.write(self.style.SUCCESS('管理员分组创建完成'))
        #4.超级管理员





