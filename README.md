# SNU 자선경매 시스템

2020년 1학기 소프트웨어 응용 수업 팀 프로젝트 용 사이트입니다.

## 요구사항

- python 3.7+
- postgresql 9.6+

## 설치

(virtualenv 사용을 권장드립니다.)

```bash
pip install -r requirements.txt
python manage.py migrate
```

## 로컬 서버 실행

```bash
python manage.py runserver
```