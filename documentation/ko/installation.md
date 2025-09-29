# 설치 가이드 (Logivore)

언어: [한국어](installation.md) | [English](../installation.md) | [繁體中文](../zh-tw/installation.md) | [简体中文](../zh-cn/installation.md)

이 문서는 Logivore를 처음부터 설치하고 배포하는 방법(Docker 및 systemd 권장 절차 포함)을 설명합니다.

## 목차
- 사전 준비
- 시스템 요구 사항
- Discord Bot 생성
- 로컬 설치(비컨테이너)
- Docker 배포(선택)
- 환경 변수(.env)
- 첫 실행
- 시스템 서비스로 실행(Linux, systemd)
- 트러블슈팅

## 사전 준비
- Python 3.8+
- Git / pip
(선택) Docker / Docker Compose, systemd(Linux), smartmontools(SMART)

## 시스템 요구 사항
- 최소: RAM 512MB, Disk 1GB, CPU 1코어, 안정적인 네트워크
- 권장: RAM 1GB+, Disk 2GB+, CPU 2코어 이상, Ubuntu 20.04+/Windows 10+/macOS 10.15+

## Discord Bot 생성
1) [Discord Developer Portal](https://discord.com/developers/applications)
2) New Application → 이름(Logivore 등)
3) Bot 탭 → Add Bot
4) Intents: Server Members / Message Content 활성화
5) Token 재발급 후 안전 저장(.env에 설정)
6) OAuth2 → URL Generator: `bot`, `applications.commands` 선택, 필요한 권한으로 서버에 초대

## 로컬 설치(비컨테이너)
```bash
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env  # DISCORD_TOKEN/OWNER_ID 등 설정
python main.py
```

## Docker 배포(선택)
Docker는 간편하지만 호스트 가시성(/ports, 상세 지표)과 일부 호스트 제어 기능이 제한될 수 있습니다. 최대 기능이 필요하면 systemd를 권장합니다.
```bash
cd deploy/docker
# 루트에서 .env 준비 권장: cp .env.example .env
docker compose up -d --build
```
기본 compose는 `network_mode: host`와 `pid: host`를 사용하고, `/var/run/docker.sock:ro`를 마운트하여 컨테이너 조회/관리를 지원합니다.

## 환경 변수(.env)
```bash
DISCORD_TOKEN=당신의봇토큰
OWNER_ID=당신의Discord사용자ID
LOG_LEVEL=INFO
LOG_FILE=logs/logivore.log
```
자세한 옵션은 `docs/configuration.md` 참고.

## 첫 실행
```
✅ Bot is ready!
✅ Logged in as: <YourBot>#1234
✅ Connected to X guilds
```
Discord에서 `/help`, `/config show`, `/monitor` 테스트.

## 시스템 서비스로 실행(Linux, systemd)
```bash
sudo nano /etc/systemd/system/logivore.service
```
```ini
[Unit]
Description=Logivore - System Monitoring Discord Bot
After=network.target

[Service]
Type=simple
User=logivore
WorkingDirectory=/home/logivore/Logivore
ExecStart=/home/logivore/Logivore/venv/bin/python main.py
Restart=always
RestartSec=10

Environment=PYTHONPATH=/home/logivore/Logivore
Environment=DISCORD_TOKEN=your_token_here
Environment=OWNER_ID=your_user_id

[Install]
WantedBy=multi-user.target
```
활성화:
```bash
sudo systemctl daemon-reload
sudo systemctl enable logivore
sudo systemctl start logivore
sudo systemctl status logivore
```
부팅 복구와 sudoers 예시는 `systemd-examples/` 및 `SETUP-RECOVERY.md` 참고.

## 트러블슈팅
- 의존성: `pip install -r requirements.txt`
- 토큰 오류: `.env`의 `DISCORD_TOKEN` 확인
- 슬래시 명령 미표시: 동기화 대기, 권한(`applications.commands`) 확인
- Docker 컨테이너 즉시 종료: `docker compose logs -f logivore` 확인, 환경 변수/볼륨 점검

디버그: `.env`의 `LOG_LEVEL=DEBUG`, 또는 `python main.py 2>&1 | tee logs/startup.log`
