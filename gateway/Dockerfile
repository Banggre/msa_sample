# Nginx 최신 버전 사용
FROM nginx:latest

# nginx.conf 설정 파일을 컨테이너의 기본 설정으로 복사
COPY nginx.conf /etc/nginx/nginx.conf

# 컨테이너 실행 시 Nginx 실행
CMD ["nginx", "-g", "daemon off;"]