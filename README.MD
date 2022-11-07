## IIEII - 추천 시스템 프로젝트

# **프로젝트 개요**

- 음악 장르 기반 추천 웹 서비스

## 목표

- 장고 DRF를 실습 하며 배운 것을 바탕으로 추천 시스템과 연동한 웹서비스 개발
- Django와 추천시스템을 연동하여 기한(2022.11.02 ~ 2022.11.08)내에 프로젝트 완성을 목표

## 주요 구현 기능

- 장고
    - 회원가입, 로그인, 로그아웃 기능 (Django custom user model 사용)
    - 플레이리스트(one-to-one, many-to-many) 모델링
    - 유저의 커스텀 플레이리스트 CRUD
    - Django Rest Framework CBV, Serializer 기능 활용

- 추천 시스템(협업필터링)
    - 장르 기반의 음악 추천 시스템

## Wireframe
    https://www.notion.so/IIEII-73143dd9bd204b8298aa8a20959279ee#fcb6972857c24292b911b1badfdee7f9

## 트러블 슈팅
Link : [트러블 슈팅 위키로 이동](https://github.com/kbm1933/B2_IIEII_DRF/wiki/Editing-%ED%8A%B8%EB%9F%AC%EB%B8%94-%EC%8A%88%ED%8C%85)

## API 명세서
- Music Play List
![music_list_api](https://user-images.githubusercontent.com/55372753/200352093-29e35d99-4170-427f-8157-2e19fab4026a.png)

- User
![music_user_api](https://user-images.githubusercontent.com/55372753/200352177-c6815724-6dcc-4744-acbb-6880cc2cf8e7.png)

## ERD
![image](https://user-images.githubusercontent.com/55372753/200350562-ebfdc612-1d8f-4cad-b71f-0cd4ca19262a.png)

## 구현 사진
 - 로그인
 ![music_login](https://user-images.githubusercontent.com/55372753/200352607-ea792024-3ce3-49a8-a52b-7392b1d9db6e.png)

 - 회원가입
 ![music_signup](https://user-images.githubusercontent.com/55372753/200352719-ef5155cf-f0cd-4b84-ac92-2f2419908077.png)

 - 음악 선택
 ![music_select](https://user-images.githubusercontent.com/55372753/200352818-2560872e-f622-4a19-87c1-dbb4b1e8d8a8.png)

 - 메인 페이지
 ![music_main](https://user-images.githubusercontent.com/55372753/200352893-dd436f41-ee32-4fa7-886c-7bf520cb7ac8.png)

 - 플레이 리스트 제작
 ![music_make_playlist](https://user-images.githubusercontent.com/55372753/200352979-3c7c0f1c-c992-4437-84c6-6dff2b8056ea.png)

 - 플레이 리스트
 ![music_user_playlist](https://user-images.githubusercontent.com/55372753/200353354-cc019edc-5523-417b-9ade-b84279c3820f.png)

 - 플레이 리스트 수정/삭제
 ![music_playlist_modify](https://user-images.githubusercontent.com/55372753/200354128-4f026489-b5f9-4f70-81e9-fbbfcd559bc3.png)

 - 유저 프로필
 ![music_user_profile](https://user-images.githubusercontent.com/55372753/200353475-dd9ebfac-7912-429c-92de-6f924ec27e70.png)

 - 유저 프로필 수정
 ![music_user_modify](https://user-images.githubusercontent.com/55372753/200353697-062d514c-79d9-4497-a6ed-e8eda540d544.png)

