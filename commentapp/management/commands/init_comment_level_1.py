from django.core.management.base import BaseCommand
from commentapp.models import Comment


class Command(BaseCommand):
    help = 'Init comment.comment_level_1'

    def handle(self, *args, **kwargs):

        count_changed = 0  # Количество измененных объектов

        for comment in Comment.objects.all():

            if comment.comment_to is None:
                # Если у комментария не заполнено поле comment_to, то значит это комментарий первого уровня
                # в таком случае поле comment_level_1 равно None
                if comment.comment_level_1 is not None:
                    comment.comment_level_1 = None
                    comment.save()
                    count_changed += 1
            else:
                # У комментария заполнено поле comment_to - значит нужно вычислить поле comment_level_1
                # Идем по цепочке ответов до тех пор пока не дойдем до комментария первого уровня
                comment_level_1_array = list()
                comment_level_1 = comment.comment_to
                while True:
                    if comment_level_1.comment_to is None:
                        # Нашли комментарий первого уровня - выходим
                        break
                    # Избегаем зацикливания если дерево в БД неправильное - просто выходим
                    if comment_level_1 in comment_level_1_array:
                        print(f"ошибка зацикливания: узел {comment_level_1.pk}:")
                        break
                    comment_level_1_array.append(comment_level_1)
                    # Поднимаемся выше по дереву
                    comment_level_1 = comment_level_1.comment_to

                if comment.comment_level_1 is None or comment.comment_level_1 != comment_level_1:
                    comment.comment_level_1 = comment_level_1
                    comment.save()
                    count_changed += 1

            # Просмотр результата
            s = f'{str(comment.pk)}'
            if comment.comment_to is not None:
                s += f' {str(comment.comment_to.pk)}'
            else:
                s += " -"
            if comment.comment_level_1 is not None:
                s += f' {str(comment.comment_level_1.pk)}'
            else:
                s += " -"
            print(s)

        print(f"Поле comment_level_1 в таблице Comment изменено в {count_changed} объектах")
