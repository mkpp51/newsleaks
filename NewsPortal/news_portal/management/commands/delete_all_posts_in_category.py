from django.core.management.base import BaseCommand

from news_portal.models import Post, Category


class Command(BaseCommand):
    help = 'Delete all publications in category'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях. Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнится при вызове вашей команды
        self.stdout.readable()
        self.stdout.write(
            f'Do you really want to delete all publications of chosen {options["category"]} category? yes/no')  # спрашиваем пользователя, действительно ли он хочет удалить все товары
        answer = input()  # считываем подтверждение

        if answer == 'yes':  # в случае подтверждения действительно удаляем все товары
            category = Category.objects.get(cat_name=options['category'])
            Post.objects.filter(post_cat=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted all publications in category {category.cat_name}'))
            return

        self.stdout.write( self.style.ERROR('Access denied'))  # в случае неправильного подтверждения, говорим, что в доступе отказано