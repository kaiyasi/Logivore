# 명령어 참고서 (Logivore)

언어: [한국어](commands.md) | [English](../commands.md) | [繁體中文](../zh-tw/commands.md) | [简体中文](../zh-cn/commands.md)

이 문서는 Logivore의 슬래시 명령을 용도/매개변수/예시와 함께 설명합니다.

## 목차
- 시스템 모니터링
- Docker 관리
- 알림 관리
- SSL 인증서
- 설정
- 봇 관리
- 도움말
- 분류/권한
- 팁/오류 처리

---

## 시스템 모니터링

### /monitor
실시간 모니터(10초마다 자동 갱신). CPU/메모리/디스크/네트워크.
- 사용법: `/monitor`

### /ports
호스트 포트 점유(Docker 매핑 + 시스템 LISTEN). 페이지 버튼, 길면 첨부로 대체.
- 사용법: `/ports`

### /top
상위 프로세스(CPU/메모리).
- 사용법: `/top [count]` (기본 10, 1–20)

### /smart
디스크 SMART 건강(Linux, smartmontools 필요).
- 사용법: `/smart`

---

## Docker 관리

### /docker status (/docker ps)
컨테이너 상태/이미지/포트/리소스.
- 사용법: `/docker status`

### /docker start / stop / restart
- 사용법: `/docker start <container>` / `stop` / `restart`

### /docker logs
컨테이너 로그 조회.
- 사용법: `/docker logs <container> [lines]` (기본 50)

### /docker stats
컨테이너 리소스 통계.
- 사용법: `/docker stats [container]`

---

## 알림 관리 (alerts)

### /alerts list
알림 목록.
- 사용법: `/alerts list`

### /alerts add
CPU/메모리/디스크/프로세스 알림 추가.
- 사용법: `/alerts add <type> <threshold> [channel]`
- type: `cpu` `memory` `disk` `process`

### /alerts remove
- 사용법: `/alerts remove <alert_id>`

### /alerts test
- 사용법: `/alerts test [type]`

---

## SSL 인증서 (ssl)

### /ssl list / check / renew / auto-renew
- 사용법: `list`, `check <domain>`, `renew <domain>`, `auto-renew <enable|disable> [days_before]`

---

## 설정 (config)

### /config show
- 사용법: `/config show [section]` (system/alerts/docker/ssl)

### /config set
- 사용법: `/config set <key> <value>` (예: `update_interval 15`)

### /config reload
- 사용법: `/config reload`

### /language (/config language)
- 사용법: `/language [language_code]` (`en`/`zh-tw`/`zh-cn`/`ko`/`ja`/`de`/`ru`)

---

## 봇 관리 (Owner 전용)
- `/restart` 재시작
- `/shutdown` 정상 종료
- `/reload <cog>` 모듈 리로드
- `/sync` 슬래시 명령 동기화
- `/status` 상태/서버수/리소스

---

## 도움말

### /help
분류별 도움말.
- 사용법: `/help [category]` (`monitoring`/`docker`/`alerts`/`ssl`/`config`/`admin`)

---

## 분류/권한
- 일반: `/monitor` `/ports` `/top` `/smart` `/docker status|logs|stats` `/ssl list|check` `/config show` `/language` `/status` `/help`
- Owner: `/docker start|stop|restart` `/alerts add|remove` `/ssl renew|auto-renew` `/config set|reload` `/restart|/shutdown|/reload|/sync`
- Discord 권한: Send Messages / Embed Links / Use Slash Commands / (필요 시) Manage Messages

---

## 팁/오류 처리
- 모니터링: `/monitor` 개요, `/alerts add`로 선제 알림
- Docker: `/status` → `logs` → `stats`
- SSL: `/ssl auto-renew enable`와 월 1회 `/ssl list`
- 설정: `/config show`/`reload`, 언어 `/language`

오류 처리:
- 권한 부족 → 필요한 권한 안내
- 잘못된 인자 → 올바른 사용 예시 제공
- 시스템 오류 → 친절한 메시지/폴백
- 네트워크 → 타임아웃/재시도
