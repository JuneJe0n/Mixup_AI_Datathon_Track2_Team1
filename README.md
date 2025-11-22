<h1 align="center"> Language Modernization Promptathon</h1>

[**Dohyeon Kim**](https://github.com/Dohyeon-Kim1) · [**Minsoo Kang**](https://github.com/Kongms002) · [**Junseok Kim**](https://github.com/koesnujmik) · [**Jiyoon Jeon**](https://github.com/JuneJe0n)


고전 한국어(한문, 한글, 영어가 섞인 고문서)를 현대 한국어로 변환하는 AI 모델을 개발하는 프로젝트입니다. LLM as a Judge 평가 시스템을 겨냥하여 최적화된 프롬프트 엔지니어링 기법을 적용하였습니다.

## 🎯 문제 정의

고전 한국어 문서를 현대 한국어로 정확하게 변환하면서, LLM as a Judge 평가 시스템(Omission/Restoration/Naturalness/Accuracy)의 점수를 최대화하는 것이 목표입니다. 기존 베이스라인 접근 방식에서 낮은 점수를 기록한 패턴을 분석하여 반대로 접근하는 전략을 취했습니다.

## 🔬 실험 방식

- **Subset 기반 평가**: 전체 데이터셋에서 부분 집합을 추출하여 다양한 실험을 반복 수행
- **반전 접근 전략**: 기존 방법에서 낮은 점수를 기록한 패턴을 분석하고 이를 반대로 적용하는 최적화 방식
- **Validation 기반 최적화**: 실시간 validation 결과를 모니터링하며 프롬프트 파라미터를 지속적으로 조정
- **Ensemble 기법**: 단일 쿼리에 대해 여러 개의 답변을 생성하고 최적의 결과를 선택

## 📋 필수 파일 설명

```
code/
├── baseline_generate.py   # 현대어 변환 문장 생성 스크립트
├── evaluate.py            # 평가 스크립트
├── metrics.py             # Omission/Restoration/Naturalness/Accuracy 기반 평가 메트릭 계산
├── prompts.py             # 프롬프트 템플릿 (이 파일을 수정하세요!)
├── pyproject.toml         # Python 의존성 관리
├── .python-version        # Python 버전 명시
├── .env.example           # 환경 변수 예시
└── data/                  # 데이터셋 디렉토리
    └── train_dataset.csv  # 학습 데이터 (여기에 넣으세요)
```

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# uv 설치 (이미 설치되어 있다면 생략)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 의존성 설치
uv sync
```


### 2. API 키 설정

# .env 파일을 열어서 API 키 입력
# UPSTAGE_API_KEY=your_actual_api_key_here

Upstage API 키는 [https://console.upstage.ai/](https://console.upstage.ai/)에서 발급받을 수 있습니다.

> 💡 **팁**: `.env` 파일은 API 키 같은 민감한 정보를 저장하는 파일이므로 Git에 커밋되지 않도록 `.gitignore`에 포함되어 있습니다.

### 3. 데이터 준비

`data/train_dataset.csv` 파일을 준비합니다. 파일은 다음 컬럼을 포함해야 합니다:
- `original_sentence`: 변환이 필요한 원문
- `answer_sentence`: 변환된 현대어 문장 (평가 시 사용)

### 4. 변환 문장 생성

```bash
# 기본 실행
uv run python baseline_generate.py

# 옵션 지정 (subset 처리: 300행부터 끝까지)
uv run python baseline_generate.py --input data/test_dataset.csv --output submission_300-400.csv --model solar-pro2
```

**주요 파라미터 설명:**
- `--input`: 입력 CSV 파일 경로 (original_sentence, id 컬럼 필수)
- `--output`: 출력 CSV 파일 경로
- `--model`: Upstage API 모델 선택 (solar-pro2 권장)

**Upstage API 활용:**
- **API 엔드포인트**: `https://api.upstage.ai/v1`
- **인증 방식**: 환경변수 `UPSTAGE_API_KEY`를 통한 API 키 인증
- **모델**: Solar Pro 2 사용으로 고품질 텍스트 생성
- **Temperature**: 0.0으로 설정하여 결정론적 결과 보장
- **Few-shot**: TF-IDF 기반 유사도 계산으로 최적의 예시 선택

생성된 `submission.csv` 파일은 다음 컬럼을 포함합니다:
- `id`: 원본 데이터의 ID
- `original_sentence`: 원문
- `answer_sentence`: AI가 변환한 문장

### 5. 평가

```bash
# 기본 실행
uv run python evaluate.py

# 옵션 지정
uv run python evaluate.py --true_df data/train_dataset.csv --pred_df submission.csv --output analysis.csv
```

평가 결과:
- 콘솔에는 Omission / Restoration / Naturalness / Accuracy 4개 카테고리의 평균 점수와 전체 평균 점수가 출력됩니다.
- 각 샘플별 상세 평가 결과는 analysis.csv 파일로 저장됩니다.
- 전체 평가 요약은 analysis_summary.txt 파일로 저장됩니다.

## 🚀 프로젝트 핵심 기능

### System Prompt 최적화

**역할(Role) 지정**: 고전 한국어 변환 전문가로 명확한 역할 부여
- "당신은 한문, 한글, 영어가 섞인 고문서를 현대 한국어로 변환하는 전문가입니다."

**명시적인 규칙 블록화 및 구조화**: 변환 원칙을 체계적으로 분류
- [의미 보존], [문체 변환], [문자 변환], [표기 변환] 등 카테고리별 구분
- 각 단계별로 구체적인 지침과 예시 제공

**강한 제약 조건 표현**: 엄격한 준수 요구사항 명시
- "다음 원칙을 엄격히 준수하세요"
- "⚠️ 필수 출력 형식"으로 강제성 부여

**입·출력 형식에 대한 명시**: 5단계 변환 과정 요구
- 1단계: 의미 파악 → 2단계: 변환 요소 식별 → 3단계: 변환 방향 결정 → 4단계: 단계별 변환 실행 → 5단계: 검증

**한 가지 쿼리에 대해 여러 개의 답을 요구하고 Ensemble**: 10개의 변환 문장 생성 후 최적 선택
- "위의 원칙을 준수하여 10개의 변환된 문장을 생성하고, 그 중에서 원본 문장의 정보 및 의미를 가장 잘 담고 있는 문장 하나만을 출력하세요."

### Few-shot Prompt 최적화

**TF-IDF 유사도 기반 Few-shot 선택**: 입력 쿼리와의 관련성 고려
- Upstage Solar Pro Tokenizer를 활용한 토큰화
- TF-IDF 벡터화를 통한 의미적 유사도 계산
- Top-5개의 가장 관련성 높은 샘플 선택

**Multi-turn 대화 형식**: Single-turn보다 더 효과적인 성능
- user-assistant 쌍으로 구성된 chat 형식 적용
- 실제 대화 맥락을 반영한 few-shot 구성

**적정 Few-shot 개수**: 너무 많은 few-shot은 system prompt의 지시를 희석시키는 것으로 확인
- 최적의 개수로 Top-5개 유지

### Temperature 설정

**결정론적 결과 보장**: 비교 가능한 실험을 위해 temperature=0.0 설정
- 동일한 입력에 대해 항상 일관된 출력 생성
- 실험 재현성과 결과 비교 가능성 확보

## 🎯 성능 개선 방법

### 프롬프트 수정

`prompts.py` 파일의 `baseline_prompt`를 수정하여 성능을 개선할 수 있습니다.

```python
baseline_prompt = (
"""
# 지시
- 여기에 더 나은 지시사항을 작성하세요
- 예시를 추가하거나 수정하세요
- 변환 기준에 대한 가이드를 제공하세요

# 변환할 문장
<원문>
{text}
<변환>
"""
    .strip()
)
```

### 실험 예시

1. **Few-shot 예시 추가**: 다양한 고어·한자 문장과 현대어 변환 예시 제공
2. **변환 기준 명시**: 의미 보존, 어휘 현대화, 기사체 톤 등 기준을 명확히 제시
3. **CoT (Chain-of-Thought)**: '해석 → 핵심 정리 → 현대어 표현'의 간단한 사고 단계 삽입
4. **시스템 메시지 수정**: 현대어 재작성 규칙을 간단히 명시하여 출력 스타일 조정

## 📊 평가 메트릭

평가는 총 4개 품질 기준에 대해 모델이 생성한 문장을 LLM이 자동 평가합니다:

- **Omission**: 원문 정보가 누락된 정도
- **Restoration**: 결손 문자 복원 정확도
- **Naturalness**: 현대 한국어로서의 자연스러움
- **Accuracy**: 의미 왜곡·불필요한 추가 정보 여부

각 카테고리는 LLM이 직접 `count` 값을 산출하며,  
오류 개수가 많을수록 낮은 점수(1.0 → 0.9 → 0.7 → …)로 변환됩니다.

최종 점수는 4개 카테고리 점수의 평균으로 계산됩니다.

## 💡 팁

1. **반복 실험**: 다양한 프롬프트를 시도하고 `analysis.csv`를 분석하여 개선점 찾기
2. **품질 분석**: `analysis.csv`에서 omission, restoration, naturalness, accuracy 중 점수가 낮은 샘플을 집중 분석
3. **모델 선택**: `--model` 옵션으로 다른 모델 시도 (예: solar-pro, solar-mini)
4. **Temperature 조정**: `baseline_generate.py`의 temperature 파라미터 조정 (기본값: 0.0)

## 🔧 문제 해결

### API 키 오류
```
ValueError: UPSTAGE_API_KEY not found in environment variables
```
→ `.env.example` 파일을 `.env`로 **이름을 변경**했는지 확인하세요!  
→ `.env` 파일에 실제 API 키가 입력되어 있는지 확인하세요.

### 컬럼 오류
```
ValueError: Input CSV must contain 'original_sentence' column
```
→ 데이터셋에 `original_sentence` 컬럼이 있는지 확인하세요.

### 길이 불일치 오류
```
ValueError: Length mismatch: truth=100 vs pred=99
```
→ 생성 과정에서 일부 샘플이 누락되었습니다. 에러 로그를 확인하세요.

## 📚 참고 자료

- Upstage API 문서: https://console.upstage.ai/docs/getting-started
- uv 문서: https://docs.astral.sh/uv/

---

**Good luck with your prompt engineering!** 🚀
