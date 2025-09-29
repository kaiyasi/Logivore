# 🛠️ 관리 가이드

언어: 한국어(본 문서) | [繁體中文](../../MANAGEMENT_GUIDE.md) | [简体中文](../zh-cn/MANAGEMENT_GUIDE.md)

## 개요

봇을 재시작하지 않고 Cog/기능을 동적으로 관리합니다.

## 🔧 명령어

- `/manage reload` — 단일 모듈 리로드
- `/manage reload_all` — 모든 모듈 리로드
- `/manage sync` — Slash 명령 동기화
- `/manage status` — 봇/시스템 상태, 모듈 목록
- `/manage logs` — 최근 로그
- `/manage restart` — 봇 재시작(systemd)
- `/manage shutdown` — 봇 종료
- `/manage eval` — 코드 실행(소유자 한정)

## 🔒 권한

관리 명령은 봇 소유자만 사용 가능.

## 🚀 예시

기능 추가: 변경 → `/manage reload` → 필요 시 `/manage sync` → 테스트 → `/manage status`

대규모 변경: `/manage reload_all` → `/manage sync` → `/manage logs`

## ⚠️ 주의 사항

- 리로드 시 모듈 내부 상태가 초기화될 수 있음
- 실패 시 상세 오류 제공
- `/manage eval`은 고권한

## 🔄 핫 리로드 장점

무중단, 빠른 검증, 영향 최소화, 장애 격리.

