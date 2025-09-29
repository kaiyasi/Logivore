# 개발 가이드

언어: 한국어 | [English](../development.md) | [繁體中文](../zh-tw/development.md) | [简体中文](../zh-cn/development.md)

이 문서는 Logivore 프로젝트에 기여하려는 개발자를 위한 실무 가이드입니다.

## 목차

- [개발 환경 설정](#개발-환경-설정)
- [프로젝트 구조](#프로젝트-구조)
- [개발 워크플로](#개발-워크플로)
- [코드 스타일 및 규칙](#코드-스타일-및-규칙)
- [테스트 프레임워크](#테스트-프레임워크)
- [아키텍처 패턴](#아키텍처-패턴)
- [기여 가이드라인](#기여-가이드라인)
- [릴리스 프로세스](#릴리스-프로세스)
- [개발 도구](#개발-도구)
- [디버깅 및 프로파일링](#디버깅-및-프로파일링)

## 개발 환경 설정

### 전제 조건

- Python 3.8 이상, Git, (선택) Docker
- 가상환경(venv/virtualenv/conda)

### 초기 설정

```bash
# 1) 저장소 클론
git clone https://github.com/kaiyasi/Logivore.git
cd Logivore

# 2) 가상환경 생성/활성화
python -m venv venv
source venv/bin/activate      # Linux/Mac
# 또는
venv\Scripts\activate        # Windows

# 3) 의존성 설치
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4) pre-commit 설정
pre-commit install

# 5) 설정 파일 준비
cp .env.example .env
cp config/bot_config.example.json config/bot_config.json

# 6) 디렉터리 생성
mkdir -p logs data/backups
```

## 프로젝트 구조

- 엔트리포인트: `main.py`
- 기능: `cogs/`
- 유틸리티: `utils/`
- 언어: `languages/`
- 테스트: `tests/`
- 문서: `docs/`

영문 가이드에 상세 구조/관계도가 수록되어 있습니다.

## 개발 워크플로

### Git Flow

```bash
main        # 프로덕션 안정
develop     # 기능 통합 브랜치
feature/*   # 신규 기능
hotfix/*    # 긴급 수정
release/*   # 릴리스 준비
```

### 작업 예시

```bash
git checkout develop && git pull
git checkout -b feature/new-monitoring
# 구현
git add . && git commit -m "feat(monitoring): add GPU temperature"
git push -u origin feature/new-monitoring
# PR → 리뷰 → develop 병합
```

### 커밋 컨벤션

Conventional Commits(feat/fix/docs/style/refactor/perf/test/chore/ci)를 사용합니다.

## 코드 스타일 및 규칙

- 타입 힌트 필수
- Lint/Format: Black, isort, flake8, mypy
- Docstring: Google 스타일

```python
from typing import Any, Dict, List, Optional, Union

async def process_data(
    data: List[Dict[str, Any]],
    config: Dict[str, str],
    timeout: Optional[float] = None
) -> Union[str, None]:
    pass
```

## 테스트 프레임워크

- Pytest 구성, 비동기 테스트, 목/픽스처
- 변경된 영역의 단위 테스트부터 폭넓은 테스트로 확장

```bash
pytest -q
pytest tests/test_utils -q
```

## 아키텍처 패턴

- Cog 기반 모듈화
- Async-first
- JSON 기반 구성 주도

## 기여 가이드라인

- 작고 초점 있는 PR
- 신규/변경 로직에 대한 테스트 포함
- 무관한 변경을 단일 PR에 혼합하지 않기

## 릴리스 프로세스

- `develop`에서 release 브랜치 파생
- CI/CD 파이프라인: 테스트, Lint, 빌드/배포
- 버저닝 및 CHANGELOG 유지

## 개발 도구

### VS Code 설정 예시

```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "100"],
  "python.sortImports.args": ["--profile", "black"],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {"source.organizeImports": true}
}
```

## 디버깅 및 프로파일링

- 구조화된 로깅과 예외 컨텍스트
- 백그라운드 태스크 트레이싱
- 메트릭/타이밍 측정과 병목 분석

