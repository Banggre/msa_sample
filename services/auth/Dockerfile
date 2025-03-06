# 베이스 이미지 설정
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일 복사
COPY requirements.txt requirements.txt
COPY app/ app/

# 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 컨테이너가 실행될 때 실행할 명령어
CMD ["python", "app/main.py"]
