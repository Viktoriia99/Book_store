# https://datascienceplus.com/building-a-book-recommender-system-the-basics-knn-and-matrix-factorization/#:~:text=Building%20A%20Book%20Recommender%20System%20%E2%80%93%20The%20Basics%2C,...%205%20Collaborative%20Filtering%20Using%20Matrix%20Factorization%20

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#                ISBN;        Title;       Author;      Year;             Publisher
books = pd.read_csv('data/Books.csv', sep=';', on_bad_lines='skip', encoding="latin-1")
books.columns = ['ISBN', 'bookTitle', 'bookAuthor', 'yearOfPublication', 'publisher']
users = pd.read_csv('data/Users.csv', sep=';', on_bad_lines='skip', encoding="latin-1")
users.columns = ['userID', 'Age']
ratings = pd.read_csv('data/Ratings.csv', sep=';', on_bad_lines='skip', encoding="latin-1")
ratings.columns = ['userID', 'ISBN', 'bookRating']

print(ratings.shape)
print(list(ratings.columns))

print(ratings.head())
'''
plt.rc("font", size=15)
# ratings.bookRating.value_counts(sort=False).plot(kind='bar')
# plt.title('Rating Distribution\n')
# plt.xlabel('Rating')
# plt.ylabel('Count')
# plt.savefig('system1.png', bbox_inches='tight')
# plt.show()

# Books data
print(books.shape)
print(list(books.columns))

# Users data
print(users.shape)
print(list(users.columns))

plt.rc("font", size=15)
users.Age.hist(bins=[0, 10, 20, 30, 40, 50, 100])
# plt.xticks([0, 10, 20, 30, 40, 50, 100])
plt.title('Age Distribution\n')
plt.xlabel('Age')
plt.ylabel('Count')
# plt.savefig('system2.png', bbox_inches='tight')
# plt.show()

# Recommendations based on rating counts
rating_count = pd.DataFrame(ratings.groupby('ISBN')['bookRating'].count())
print(rating_count.sort_values('bookRating', ascending=False).head())


most_rated_books = pd.DataFrame(['0971880107', '0316666343', '0385504209', '0060928336', '0312195516'], index=np.arange(5), columns = ['ISBN'])
Most_rated_books_summary = pd.merge(most_rated_books, books, on='ISBN')
print(Most_rated_books_summary)

# Рекомендации, основанные на корреляциях / коэффициент корреляции Пирсона R
# для измерения линейной корреляции между рейтингами двух книг.
average_rating = pd.DataFrame(ratings.groupby('ISBN')['bookRating'].mean())
average_rating['ratingCount'] = pd.DataFrame(ratings.groupby('ISBN')['bookRating'].count())
print(average_rating.sort_values('ratingCount', ascending=False).head())
# Наблюдения: В этом наборе данных книга, получившая наибольшее количество оценок,
# вообще не получила высокой оценки. В результате, если бы мы использовали рекомендации,
# основанные на подсчетах рейтингов, мы бы обязательно допустили здесь ошибки.
# Итак, нам нужна лучшая система.

# Для обеспечения статистической значимости исключаются пользователи
# с рейтингом менее 200 и книги с рейтингом менее 100.
counts1 = ratings['userID'].value_counts()
ratings = ratings[ratings['userID'].isin(counts1[counts1 >= 200].index)]
counts = ratings['bookRating'].value_counts()
ratings = ratings[ratings['bookRating'].isin(counts[counts >= 100].index)]

# Rating matrix
ratings_pivot = ratings.pivot(index='userID', columns='ISBN').bookRating
userID = ratings_pivot.index
ISBN = ratings_pivot.columns
print(ratings_pivot.shape)
print(ratings_pivot.head())

bones_ratings = ratings_pivot['0316666343']
similar_to_bones = ratings_pivot.corrwith(bones_ratings)
corr_bones = pd.DataFrame(similar_to_bones, columns=['pearsonR'])
corr_bones.dropna(inplace=True)
corr_summary = corr_bones.join(average_rating['ratingCount'])
print(corr_summary[corr_summary['ratingCount']>=300].sort_values('pearsonR', ascending=False).head(10))

books_corr_to_bones = pd.DataFrame(['0312291639', '0316601950', '0446610038', '0446672211', '0385265700', '0345342968', '0060930535', '0375707972', '0684872153'],
                                  index=np.arange(9), columns=['ISBN'])
corr_books = pd.merge(books_corr_to_bones, books, on='ISBN')
print(corr_books)
'''


# Совместная фильтрация с использованием k-ближайших соседей (kNN)
combine_book_rating = pd.merge(ratings, books, on='ISBN')
columns = ['yearOfPublication', 'publisher', 'bookAuthor']
combine_book_rating = combine_book_rating.drop(columns, axis=1)
print(combine_book_rating.head())

combine_book_rating = combine_book_rating.dropna(axis = 0, subset = ['bookTitle'])

# We then group by book titles and create a new column for total rating count.
book_ratingCount = (combine_book_rating.
     groupby(by = ['bookTitle'])['bookRating'].
     count().
     reset_index().
     rename(columns = {'bookRating': 'totalRatingCount'})
     [['bookTitle', 'totalRatingCount']]
    )
print(book_ratingCount.head())

rating_with_totalRatingCount = combine_book_rating.merge(book_ratingCount, left_on = 'bookTitle', right_on = 'bookTitle', how = 'left')
print(rating_with_totalRatingCount.head())

pd.set_option('display.float_format', lambda x: '%.3f' % x)
print(book_ratingCount['totalRatingCount'].describe())

print(book_ratingCount['totalRatingCount'].quantile(np.arange(.9, 1, .01)))

popularity_threshold = 50
rating_popular_book = rating_with_totalRatingCount.query('totalRatingCount >= @popularity_threshold')
print(rating_popular_book.head())

# Filter to users in US and Canada only
combined = rating_popular_book.merge(users, left_on = 'userID', right_on = 'userID', how = 'left')
us_canada_user_rating = combined
us_canada_user_rating=us_canada_user_rating.drop('Age', axis=1)
print(us_canada_user_rating.head())

# Implementing kNN
# Finding the Nearest Neighbors
from scipy.sparse import csr_matrix
us_canada_user_rating = us_canada_user_rating.drop_duplicates(['userID', 'bookTitle'])
'''
us_canada_user_rating_pivot = us_canada_user_rating.pivot(index = 'bookTitle', columns = 'userID', values = 'bookRating').fillna(0)
us_canada_user_rating_matrix = csr_matrix(us_canada_user_rating_pivot.values)

from sklearn.neighbors import NearestNeighbors

model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
print(model_knn.fit(us_canada_user_rating_matrix))


query_index = np.random.choice(us_canada_user_rating_pivot.shape[0])

# Перетворення Pandas Series у NumPy масив і потім використання методу reshape
query_index_series = us_canada_user_rating_pivot.iloc[query_index, :].values.reshape(1, -1)

# Використання моделі KNN для знаходження сусідів
distances, indices = model_knn.kneighbors(query_index_series, n_neighbors=6)

for i in range(0, len(distances.flatten())):
    if i == 0:
        print('Recommendations for {0}:\n'.format(us_canada_user_rating_pivot.index[query_index]))
    else:
        print('{0}: {1}, with distance of {2}:'.format(i, us_canada_user_rating_pivot.index[indices.flatten()[i]], distances.flatten()[i]))
'''

# Collaborative Filtering Using Matrix Factorization
us_canada_user_rating_pivot2 = us_canada_user_rating.pivot(index = 'userID', columns = 'bookTitle', values = 'bookRating').fillna(0)
print(us_canada_user_rating_pivot2.head())

print(us_canada_user_rating_pivot2.shape)

X = us_canada_user_rating_pivot2.values.T
print(X.shape)

import sklearn
from sklearn.decomposition import TruncatedSVD

SVD = TruncatedSVD(n_components=12, random_state=17)
matrix = SVD.fit_transform(X)
print(matrix.shape)

import warnings
warnings.filterwarnings("ignore",category =RuntimeWarning)
corr = np.corrcoef(matrix)
print(corr.shape)

us_canada_book_title = us_canada_user_rating_pivot2.columns
us_canada_book_list = list(us_canada_book_title)
coffey_hands = us_canada_book_list.index("The Green Mile: Coffey's Hands (Green Mile Series)")
print(coffey_hands)

corr_coffey_hands  = corr[coffey_hands]
print(list(us_canada_book_title[(corr_coffey_hands>0.9)]))