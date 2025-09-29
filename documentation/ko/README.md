# 🤖 Logivore

Languages: [English](README.md) | [繁體中文](README.zh-tw.md) | [简体中文](README.zh-cn.md) | [日本語](README.ja.md) | 한국어 | [Deutsch](README.de.md) | [Русский](README.ru.md)

<div align="center">

**고급 시스템 모니터링 및 관리 Discord 봇**

*포괄적인 실시간 모니터링, 지능형 알림 및 자동화된 시스템 관리*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Discord.py](https://img.shields.io/badge/discord.py-2.0+-green.svg)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Made by](https://img.shields.io/badge/Made%20by-Serelix%20Studio-purple.svg)](https://serelix.xyz)

[🚀 빠른 시작](#-빠른-시작) • [✨ 기능](#-기능) • [🌍 언어](#-지원-언어) • [📖 문서](#-문서) • [💬 지원](#-지원)

</div>

## 📋 개요

Logivore는 포괄적인 시스템 모니터링 및 관리를 위해 설계된 강력한 Discord 봇입니다. 고급 자동화 기능으로 구축되어 서버 인프라에 대한 실시간 통찰력을 제공하며 엔터프라이즈급 안정성과 보안을 유지합니다.

### 🎯 주요 기능

- **🔍 실시간 시스템 모니터링** - CPU, 메모리, 디스크, 네트워크 통계
- **🚨 지능형 알림 시스템** - 시스템 문제에 대한 사전 알림
- **🐳 Docker 관리** - 완전한 컨테이너 라이프사이클 관리
- **🔄 서비스 복구** - 시스템 이벤트 후 자동 서비스 복원
- **⚡ SSL 인증서 관리** - 자동화된 인증서 모니터링 및 갱신
- **🌐 다국어 지원** - 현지화된 인터페이스로 8개 언어 지원

## ✨ 기능

### 🖥️ 시스템 모니터링
```
실시간 업데이트가 있는 대시보드
네트워크 포트 모니터링
디스크 상태 확인 (SMART)
프로세스 관리 및 모니터링
```

### 🚨 알림 관리
```
CPU/메모리/디스크 사용량 알림
프로세스 감시 모니터링
사용자 정의 임계값 구성
다중 채널 알림 지원
```

### 🐳 Docker 통합
```
컨테이너 상태 모니터링
시작/중지/재시작 작업
리소스 사용량 추적
로그 관리
```

### 🛡️ 시스템 관리
```
예약된 시스템 재부팅
서비스 복구 자동화
SSL 인증서 모니터링
Nginx Proxy Manager 통합
```

## 🌍 지원 언어

<div align="center">

| 언어 | 코드 | 상태 |
|----------|------|--------|
| 🇺🇸 English | `en` | ✅ 완료 |
| 🇹🇼 繁體中文 | `zh`/`zh-tw` | ✅ 완료 |
| 🇨🇳 简体中文 | `zh-cn` | ✅ 완료 |
| 🇰🇷 한국어 | `ko` | ✅ 완료 |
| 🇯🇵 日本語 | `ja` | ✅ 완료 |
| 🇩🇪 Deutsch | `de` | ✅ 완료 |
| 🇷🇺 Русский | `ru` | ✅ 완료 |

</div>

## 🚀 빠른 시작

### 전제 조건
- Python 3.8+
- Discord Bot Token
- Linux/Windows/macOS 시스템

### 설치
```bash
# 저장소 클론
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore

# 의존성 설치
pip install -r requirements.txt

# 환경 구성
cp .env.example .env
# Discord 봇 토큰 및 설정으로 .env 편집

# 봇 실행
python main.py
```

### Docker 배포 (선택)
```bash
cd deploy/docker
docker compose up -d --build
```

## 🏗️ 아키텍처

### 🔧 기술 스택
- **백엔드 프레임워크**: discord.py 2.0+를 사용한 Python 3.8+
- **시스템 모니터링**: psutil, subprocess 통합
- **컨테이너 관리**: Docker API 통합
- **SSL 관리**: Nginx Proxy Manager와 Let's Encrypt
- **국제화**: JSON 기반 다국어 시스템
- **구성**: 핫 리로드 기능이 있는 JSON

### 📦 핵심 모듈
```
├── 🔍 시스템 모니터링     - 실시간 시스템 통계
├── 🚨 알림 시스템        - 사전 모니터링 알림
├── 🐳 Docker 관리       - 컨테이너 라이프사이클 제어
├── 🔄 서비스 복구        - 자동 서비스 복원
├── 🛡️ SSL 관리         - 인증서 모니터링 및 갱신
├── ⚙️ 구성             - 동적 설정 관리
├── 🤖 봇 관리          - 관리 제어
└── 📚 도움말 시스템      - 대화형 문서
```

## 📖 문서

- **[설치 가이드](../installation.md)** - 단계별 설정 지침
- **[구성 참조](../configuration.md)** - 완전한 설정 문서
- **[명령어 참조](../commands.md)** - 사용 가능한 모든 봇 명령어
- **[API 문서](../api.md)** - 통합 및 확장 가이드
- **[문제 해결](../troubleshooting.md)** - 일반적인 문제 및 해결책
- 추가 가이드:
  - **[Embed 포맷팅 가이드](../ko/EMBED_FORMAT_GUIDE.md)**
  - **[관리 가이드](../ko/MANAGEMENT_GUIDE.md)**
  - **[재부팅 후 자동 복구 설정](../ko/SETUP-RECOVERY.md)**

## 🤝 기여

기여를 환영합니다! 자세한 내용은 [기여 가이드라인](CONTRIBUTING.md)을 참조하세요.

### 개발 환경 설정
```bash
# 개발 환경 클론 및 설정
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore

# 개발 의존성 설치
pip install -r requirements-dev.txt

# 테스트 실행
python -m pytest tests/
```

## 📝 라이선스

이 프로젝트는 MIT 라이선스에 따라 라이선스됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 💬 지원

<div align="center">

### 🔗 커뮤니티 및 지원

[![GitHub Issues](https://img.shields.io/badge/GitHub-Issues-red.svg)](https://github.com/kaiyasi/Logivore/issues)
[![GitHub Discussions](https://img.shields.io/badge/GitHub-Discussions-blue.svg)](https://github.com/kaiyasi/Logivore/discussions)
[![Discord](https://img.shields.io/badge/Discord-Community-purple.svg)](https://discord.gg/serelix)
[![Email](https://img.shields.io/badge/Email-Support-green.svg)](mailto:serelixstudio@gmail.com)

</div>

### 📞 연락처 정보

- **공식 웹사이트**: [https://serelix.xyz](https://serelix.xyz)
- **GitHub 저장소**: [https://github.com/kaiyasi/Logivore](https://github.com/kaiyasi/Logivore)
- **이메일**: serelixstudio@gmail.com
- **인스타그램**: [@serelix.studio](https://instagram.com/serelix.studio)

---

<div align="center">

**❤️로 만든 [Serelix Studio](https://serelix.xyz)**

*지능형 자동화를 통한 서버 관리 역량 강화*

</div>
