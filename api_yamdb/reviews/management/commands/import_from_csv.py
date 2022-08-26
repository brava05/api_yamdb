import csv

from django.core.management.base import BaseCommand

from reviews.models import Review, Comment, Category
from reviews.models import Genre, Title, TitleGenre, User


class Command(BaseCommand):
    help = 'import from csv'

    def handle(self, *args, **options):
        self.import_obj('category', Category)
        self.import_obj('genre', Genre)
        self.import_obj('titles', Title)
        self.import_obj('users', User)
        self.import_obj('review', Review)
        self.import_obj('comments', Comment)
        self.import_obj('genre_title', TitleGenre)

    def import_obj(self, name_in_file, class_name):
        file_name = f'static\data\{name_in_file}.csv'
        with open(file_name, encoding='utf-8') as r_file:
            file_reader = csv.DictReader(r_file, delimiter=",")
            count = 0
            for row in file_reader:
                if count == 0:
                    print(f'Файл содержит столбцы: {", ".join(row)}')
                if not class_name.objects.filter(pk=row.get("id")).exists():
                    if class_name == Category or class_name == Genre:
                        obj = class_name(**row)
                        obj.save()
                    elif class_name == Title:
                        obj = class_name(pk=row['id'],
                                         name=row['name'],
                                         year=row['year']
                                         )
                        obj.category = Category.objects.get(
                            pk=row.get("category")
                        )
                        obj.save()
                        # DummyModel.objects.create(**data_dict)
                    elif class_name == User:
                        obj = class_name(pk=row['id'],
                                         username=row['username'],
                                         email=row['email'],
                                         role=row['role']
                                         )
                        obj.save()
                    elif class_name == Review:
                        obj = class_name(pk=row['id'],
                                         text=row['text'],
                                         pub_date=row['pub_date'],
                                         score=row['score']
                                         )
                        obj.title = Title.objects.get(pk=row.get("title_id"))
                        obj.author = User.objects.get(pk=row.get("author"))
                        obj.save()
                    elif class_name == Comment:
                        obj = class_name(pk=row['id'],
                                         text=row['text'],
                                         pub_date=row['pub_date']
                                         )
                        obj.review = Review.objects.get(
                            pk=row.get("review_id"))
                        obj.author = User.objects.get(pk=row.get("author"))
                        obj.save()
                    elif class_name == TitleGenre:
                        obj = class_name(pk=row['id'])
                        obj.title = Title.objects.get(pk=row.get("title_id"))
                        obj.genre = Genre.objects.get(pk=row.get("genre_id"))
                        obj.save()
                else:
                    # obj = class_name.objects.get(pk=row.get("id"))
                    print('----')
                # print(obj)
                count += 1
