from .models import Category


# ---------- Список категорий  -----------------------
def menu(context):  # аргумент context передается в контекст прцесс
    categories_nav = Category.objects.all()  # Извлекаю все категории
    return {'categories': categories_nav}  # Передаю словарь с содержание категорий
