# 유기동물 봉사 활동 관리 시스템

## 시스템 구성
- Auth Service (8080): 사용자 인증 관리
- Activity Service (8081): 봉사활동/입양 활동 관리 
- Reward Service (8082): 활동 보상 관리
- API Gateway (8000): 서비스 라우팅
- MongoDB: 각 서비스별 독립 데이터베이스

## 데이터베이스 스키마

### Auth Service (volunteer_db)
- users: 사용자 정보를 기록하는 컬렉션
  - email: 사용자 이메일
  - password: 비밀번호

### Activity Service (activity_db) 
- activity: 활동 종류를 저장하는 컬렉션
  - name: 활동 이름
  - type: 활동 유형 (Volunteering/Adoption)
- user_activity_rewards: 사용자 활동 및 보상 여부를 기록하는 컬렉션
  - user_id: 사용자 ID
  - activity_id: 활동 ID
  - rewarded: 보상 지급 여부
  - created_at: 활동 일시

### Reward Service (reward_db)
- rewards: 유저별 보상 정보를 기록하는 컬렉션
  - user_id: 사용자 ID
  - point: 보상 포인트

## 시작하기

### 사전 준비사항
- Docker 및 Docker Compose 설치
- Git 설치

### 실행 방법

1. 서비스 시작
- docker-compose up --build

2 참고
- 처음 docker-compose up --build 실행 시 mongo-init에 정의 된 기본 데이터가 DB에 추가됨.

## API 명세

### Auth Service (8080)

#### 사용자 관리
- POST /auth/signup
  - 사용자 등록
  - Request Body: { "email": string, "password": string }
  - Response: {
        "message": string,
        "user_id": string
    }
  - Status: 201 Created, 400 Bad Request

- GET /auth/login  
  - 로그인
  - Request Body: { "email": string, "password": string }
  - Response: {
        "message": string,
        "user_id": string
    }
  - Status: 200 OK, 401 Unauthorized

### Activity Service (8081)

#### 활동 관리
- POST /activity/add
  - 새로운 활동 등록
  - Request Body: { "name": string, "type": "Volunteering"|"Adoption" }
  - Response: {
        "message": string,
        "activity_id": string
    }
  - Status: 201 Created, 400 Bad Request, 500 Internal Server Error

- GET /activity/get
  - 활동 정보 조회
  - Query Parameters: name=string
  - Response: {
        "message": string,
        "activity": {
            "id": string,
            "name": string,
            "type": "Volunteering"|"Adoption"
        }
    }
  - Status: 200 OK, 404 Not Found, 500 Internal Server Error

#### 사용자 활동 관리
- POST /activity/add_user_activity_rewards
  - 사용자 활동 기록
  - Request Body: { "user_id": string, "activity_id": string }
  - Response: { "message": string }
  - Status: 201 Created, 500 Internal Server Error

- GET /activity/get_user_activity_rewards
  - 사용자 활동 내역 조회
  - Request Body: { "user_id": string }
  - Response: {
        "message": string,
        "user_activity_rewards": [
            {
                "id": string,
                "activity_name": string,
                "activity_type": "Volunteering"|"Adoption",
                "activity_id": string,
                "created_at": datetime,
                "rewarded": boolean
            }
        ]
    }
  - Status: 200 OK, 500 Internal Server Error

- POST /activity/update_user_activity_rewards
  - 사용자 활동 보상 상태 업데이트
  - Request Body: { 
        "activity_id_list": string[],
        "rewarded": boolean
    }
  - Response: { "message": string }
  - Status: 200 OK, 500 Internal Server Error

### Reward Service (8082)

#### 보상 관리
- POST /reward/handle_reward
  - 활동에 대한 보상 계산 및 지급
  - Request Body: { "user_id": string }
  - Response: {
        "success": boolean,
        "message": string,
        "adoption_count": number,
        "volunteering_count": number,
        "points_earned": number
    }
  - Status: 200 OK, 500 Internal Server Error

### API Gateway (8000)
- 모든 서비스 엔드포인트는 API Gateway를 통해 라우팅됨
- 요청 형식: http://localhost:8000/{service}/{endpoint}
- 예시: http://localhost:8000/auth/login

