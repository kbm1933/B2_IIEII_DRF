import os
import django
import pandas as pd
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from musicplaylist.models import Music, PlayList

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wetyle_share.settings')
django.setup()

# 유사도 구하는 함수
def recommend_music_list(music_title, top=10):
    # 추천리스트
    dbtest_musics = Music.objects.all().values()
    dbtest_musics_pandas = pd.DataFrame(dbtest_musics)

    # 장르 데이터 벡터화
    counter_vector = CountVectorizer(ngram_range=(1,2), encoding=u'utf-8')
    c_vector_genres = counter_vector.fit_transform(dbtest_musics_pandas['music_genre'])
    # print(c_vector_genres.shape)
    # print(counter_vector.vocabulary_) #장르 인덱스 확인

    similarity_genre = cosine_similarity(c_vector_genres, c_vector_genres)
    # print(similarity_genre.shape)

    target_music_index = dbtest_musics_pandas[dbtest_musics_pandas['music_title'] == music_title].index.values

    dbtest_musics_pandas['similarity'] = similarity_genre[target_music_index, :].reshape(-1,1)

    temp = dbtest_musics_pandas.sort_values(by='similarity', ascending=False)
    final_index = temp.index.values[ :top]
    return dbtest_musics_pandas.iloc[final_index]

def random_choice(user_id):
    # 사용자가 취향으로 선택한 플레이 리스트에서 한곡을 랜덤 선택 (제목)
    myselect = PlayList.objects.get(playlist_user_id=user_id, is_main=True)   # 사용자의 대표 플레이 리스트
    myselect_title = myselect.playlist_select_musics.values("music_title")
    myselect_list = list(myselect_title)

    choice_music = random.choice(myselect_list)
    return choice_music