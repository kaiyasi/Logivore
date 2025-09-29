# 트러블슈팅 (Logivore)

언어: [한국어](troubleshooting.md) | [English](../troubleshooting.md) | [繁體中文](../zh-tw/troubleshooting.md) | [简体中文](../zh-cn/troubleshooting.md)

systemd / Docker 환경에서 발생하는 흔한 문제와 해결 방법을 정리했습니다.

## 목차
- 빠른 점검
- 로그/상태 확인
- 시작 문제
- 명령/권한 문제
- Docker 관련
- systemd 서비스
- SSL/인증서
- 알림
- 성능
- 에러 코드
- 복구
- FAQ

---

## 빠른 점검
1) `.env`의 `DISCORD_TOKEN`/`OWNER_ID` 정확성
2) `pip install -r requirements.txt`
3) 권한: Send Messages / Embed Links / Use Slash Commands
4) 경로: `logs/` `config/` 쓰기 가능, Docker 볼륨
5) 언어: `DEFAULT_LANGUAGE`에 해당하는 파일 존재

## 로그/상태 확인
```bash
tail -f logs/logivore.log
python main.py 2>&1 | tee logs/startup.log
cd deploy/docker && docker compose logs -f logivore
```

슬래시 명령 동기화는 수십 초가 걸릴 수 있습니다.

## 시작 문제
- 토큰 무효: Developer Portal에서 재발급, `.env` 업데이트
- 의존성: `pip install -r requirements.txt`
- Python 버전: 3.8+
- 슬래시 명령 없음: `applications.commands` 권한, 봇이 서버에 있는지 확인

## 명령/권한 문제
- 전송/임베드 불가: 채널 권한 확인
- Owner 전용: `.env`의 `OWNER_ID`가 본인 ID인지 확인
- 400 Bad Request(길이 제한): 출력 분할/첨부로 대체(재발 시 사례 공유)

## Docker 관련
- 컨테이너 즉시 종료: `docker compose logs -f logivore`로 원인 확인
- 가시성 부족: `network_mode: host` / `pid: host` 사용
- `/ports` 중복: IPv4/IPv6 통합 표시(IP: v4/v6/*)

## systemd 서비스
```bash
sudo systemctl status logivore
sudo journalctl -u logivore -f
```
- `ExecStart`/`WorkingDirectory`/`User` 확인
- 부팅 복구: `systemd-examples/`, `SETUP-RECOVERY.md`

## SSL/인증서
- NPM 컨테이너명, `SSL_CERT_PATH`, OpenSSL 가능 여부
- DNS(A/AAAA) 및 Let’s Encrypt 제한

## 알림
- 임계값(0–100), `alert_interval`, `alert_channel` 확인
- 권장: CPU/메모리 80–90%, 디스크 85–95%

## 성능
- 주기 늘리기: `UPDATE_INTERVAL` / `ALERT_INTERVAL`
- 기능 축소: Docker 모니터링/패널 수 줄이기
- OS 측 확인: top/htop

## 에러 코드
- 50035 Invalid Form Body: 길이 제한 초과(보호 로직 있음)
- LoginFailure: 토큰 무효
- Missing Permissions: 권한 부족
- JSONDecodeError: config.json 문법 오류

## 복구
- 백업: `cp -r config logs backups/$(date +%F_%T)`
- 복원: 필요한 경우 덮어쓰기
- 재시작: 서비스/컨테이너

## FAQ
- 동기화 지연? → 수십 초 대기, 재시작, 권한 확인
- `/ports` 너무 김? → 분할/첨부 처리, 사례 공유 요청
- Docker 보안? → read_only/no-new-privileges/tmpfs/docker.sock:ro 전제, 환경에 맞게 조정

