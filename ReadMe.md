Docker-compose를 이용
$ docker-compose up (이미지 빌드가 필요할시 --build 옵션을 이용)
$ docker-compose stop

개발환경이라 tty모드로 실행

## migrate 하는 법

1. 
python3 manager.py initdb 를 이용하여 첫 db 초기화 (migration을 하기위한 부분이므로 첫 초기화 떄 1번만 실행)

이후 아래 명령어를 차례로 실행
2. 
python3 manager.py db migrate --message 'migrate msg'
3. 
manager.py db upgrade

## 블록체인(BlockChain)
### 1.
블록체인의 경우 Chain을 sync시 내부 파일로 저장
3개의 블록 체인 컨테이너를 띄우고 서로 데이터를 주고 받을 수 있도록

## 선거(Election)
### 1.
일단 models는 연결 완료. 개발용으로 쓸 dev 서버가 있으면 좋을 것 같음.

