
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#                ISBN;        Title;       Author;      Year;             Publisher
'''
books = pd.read_csv('data2/Books.csv', sep=',', on_bad_lines='skip', encoding="latin-1", low_memory=False)
books.columns = ['ISBN', 'bookTitle', 'bookAuthor', 'yearOfPublication', 'publisher', 'imageUrlS', 'imageUrlM', 'imageUrlL', 'price', 'count']
users = pd.read_csv('data2/Users.csv', sep=',', on_bad_lines='skip', encoding="latin-1") 
users.columns = ['userID', 'Location', 'Age']
ratings = pd.read_csv('data2/Ratings.csv', sep=',', on_bad_lines='skip', encoding="latin-1")
ratings.columns = ['userID', 'ISBN', 'bookRating']

print(ratings.shape)
print(list(ratings.columns))

# Підрахунок пропущених значень у кожному наборі даних
missing_books = books.isnull().sum()
missing_users = users.isnull().sum()
missing_ratings = ratings.isnull().sum()

# Виведення результатів
print(f"Пропущених значень у наборі даних books: \n{missing_books}")
print(f"Пропущених значень у наборі даних users: \n{missing_users}")
print(f"Пропущених значень у наборі даних ratings: \n{missing_ratings}")


print(books.head())'''
#
# import numpy as np
#
# # Читання даних з CSV-файлу
# books = pd.read_csv('data2/Books.csv', sep=',', on_bad_lines='skip', encoding="latin-1", low_memory=False)
#
# # Додавання стовпця з випадковою ціною
# books['Price'] = np.random.uniform(50, 500, books.shape[0]).round(2)
#
# # Додавання стовпця з випадковою кількістю
# books['Count'] = np.random.randint(0, 51, books.shape[0])
#
# # Збереження оновлених даних у CSV-файл
# books.to_csv('data2/Books.csv', index=False, encoding='latin-1')
