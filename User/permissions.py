from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from Book.models import Book


def group_permissions():
    teacher_group, created = Group.objects.get_or_create(name="Teacher")
    student_group, created = Group.objects.get_or_create(name="Student")

    content_type = ContentType.objects.get_for_model(Book)
    post_permission = Permission.objects.filter(content_type=content_type)

    for permission in post_permission:
        if permission.codename == "view_book":
            student_group.permissions.add(permission)
            teacher_group.permissions.add(permission)
        else:
            teacher_group.permissions.add(permission)

    student_group.save()
    teacher_group.save()


        
