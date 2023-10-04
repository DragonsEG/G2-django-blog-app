from django import template
from blog.models import company
register = template.Library()


@register.filter(name='is_viewer')
def is_viewer(user):
    return user.groups.filter(name='User-Group').exists()


@register.filter(name='is_admin')
def is_admin(user):
    return user.groups.filter(name='Admin-Group').exists()


@register.filter(name='category')
def category(categories, category):
    return categories[category]


@register.filter(name='permission')
def permission(user, wantedPermission):
    Groups = user.groups.all()
    for group in Groups:
        if group.permissions.all().filter(codename=wantedPermission).exists():
            return True
    return False


@register.filter(name="is_company")
def is_company(user):
    return company.objects.all().filter(name=user).exists()
