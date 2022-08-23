import csv
from unicodedata import name

class Category(object):
    id: int
    name: str
    slug: str
    
    def __init__(self, *args):
        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
    
    def __str__(self) -> str:
        return(f'{self.id} {self.name} {self.slug}')

def import_obj(name_in_file, class_name):

    file_name = f'static\data\{name_in_file}.csv'
    with open(file_name, encoding='utf-8') as r_file:
        file_reader = csv.DictReader(r_file, delimiter = ",")
        count = 0
        for row in file_reader:
            if count == 0:
                print(f'Файл содержит столбцы: {", ".join(row)}')
                # list_of_attributes = row.split(',')
                # print(list_of_attributes)
            # print(f' {row["id"]} - {row["name"]} - {row["slug"]}')
            print(row)
            e = class_name(row)
            print(e)
            count += 1

if __name__ == '__main__':
    import_obj('category', Category)