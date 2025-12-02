<div align="center">
<h1 > Language Modernization Promptathon </h1>

[**Dohyeon Kim**](https://github.com/Dohyeon-Kim1) · [**Minsoo Kang**](https://github.com/Kongms002) · [**Junseok Kim**](https://github.com/koesnujmik) · [**Jiyoon Jeon**](https://github.com/JuneJe0n)
</div>

이 프로젝트는 Solar Pro 2 API를 활용하여 오로지 프롬프트만으로 한문/한글/영어가 섞인 문장을 현대 문장으로 변환하는 프롬프톤입니다. <br>
모델 튜닝이 아닌 프롬프트 엔지니어링만으로 교정 태스크를 해결하는 것이 목표입니다. <br>

<h2>Problem Definition</h2>

고전 한국어(한문, 한글, 영어가 섞인 고문서)를 현대 한국어로 변환하는 AI 모델을 개발하고자 하였습니다. <br>
GT와 유사하게 깔끔한 줄글로 만들고자 하면 llm as a judge의 score가 낮게 나오는 것을 확인하고, output을 최대한 풍부하게 생성하며  llm as a judge 평가 시스템을 겨냥한 프롬프트 엔지니어링 기법을 적용하였습니다.

<br>

<h2>Experimental Methods</h2
                            
**1) Train Data Subset 기반의 효율적 실험 설계** <br>
전체 데이터셋을 매번 사용하는 것은 시간적·자원적 비용이 크기 때문에, 데이터의 분포를 대표할 수 있는 Subset(부분 집합)을 전략적으로 추출하였습니다.  <br>
이를 통해 실험 사이클을 단축시키고, 다양한 방법론을 빠르게 테스트하여 실험의 다양성을 확보했습니다. <br>

**2) 실패 사례 분석을 통한 역발상적 접근** <br>
단순히 점수가 낮은 방법론을 배제하는 것에 그치지 않고, '왜 점수가 낮은가'를 분석했습니다. 성능 저하를 유발하는 논리나 접근 방식을 파악한 뒤, 이를 정반대의 메커니즘으로 뒤집어 적용해보는 실험을 수행했습니다. <br>
이 과정에서 유의미한 성능 향상 포인트를 발견할 수 있었습니다. 

**3) 검증(Validation) 기반 프롬프트 최적화 (Iterative Refinement)** <br>
실험의 각 단계마다 산출되는 결과를 실시간으로 모니터링하며 피드백 루프를 구축했습니다.<br>
정량적 지표뿐만 아니라 모델의 생성 결과물을 정성적으로 확인하며, 모델이 의도대로 동작하도록 프롬프트 최적화(Prompt Optimization)를 반복적으로 수행하여 최종 성능을 극대화했습니다.

<br>

<h2> File tree </h2>

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

<h2> 🚀 Getting Started </h2>

<h3>1. Environment Setup</h3>

```bash
# uv 설치 (이미 설치되어 있다면 생략)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 의존성 설치
uv sync
```

<h3>2. Configuring the API Key </h3>

```bash
# .env 파일을 열어서 API 키 입력
UPSTAGE_API_KEY=your_actual_api_key_here
```

Upstage API 키는 [https://console.upstage.ai/](https://console.upstage.ai/)에서 발급받을 수 있습니다.

<h3>3. Data Preperation</h3>

`data/train_dataset.csv` 파일을 준비합니다. 파일은 다음 컬럼을 반드시 포함해야 합니다:
- `original_sentence`: 변환이 필요한 원문
- `answer_sentence`: 변환된 현대어 문장 (평가 시 사용)

<h3>4. Inference </h3>

```bash
# 기본 실행
uv run python baseline_generate.py

# 옵션 지정 (subset 처리: 300행부터 끝까지)
uv run python baseline_generate.py --input data/test_dataset.csv --output submission_300-400.csv --model solar-pro2
```

**parameter description:**
- `--input`: 입력 CSV 파일 경로 (original_sentence, id 컬럼 필수)
- `--output`: 출력 CSV 파일 경로
- `--model`: Upstage API 모델 선택 (solar-pro2 권장)

생성된 `submission.csv` 파일은 다음 컬럼을 포함합니다:
- `id`: 원본 데이터의 ID
- `original_sentence`: 원문
- `answer_sentence`: AI가 변환한 문장

### 5. Evaluation

```bash
# 기본 실행
uv run python evaluate.py

# 옵션 지정
uv run python evaluate.py --true_df data/train_dataset.csv --pred_df submission.csv --output analysis.csv
```

<h2> 📍 Core Features</h2>

**1) System Prompt** <br>
모델의 **역할(Role)을 구체적으로 지정**하였으며, 지시 사항이 누락되지 않도록 핵심 규칙을 블록(Block) 단위로 구조화했습니다. <br>
특히, 모델이 지켜야 할 강한 제약 조건과 입·출력 형식(Format)을 명시했습니다. 또한, 인간의 **메타인지** 구조를 차용. 1) 입력 이해 → 2) 1차 판단 → 3) 자기 비판·재검토 → 4) 최종 판단+이유 → 5) 전체 과정에 대한 신뢰도 평가까지 5단계 자기 성찰형 프롬프트를 활용하였습니다. 그리고 대화의 맥락(fewshot)을 충분히 활용하도록 지시했습니다.

**2) Few-shot Prompting** <br>
고정된 예시를 사용하는 대신, 입력되는 Query와 데이터셋 내 샘플 간의 **TF-IDF 유사도**를 계산하여 가장 연관성이 높은 상위 5개의 샘플을 동적으로 추출해 Few-shot으로 활용했습니다. <br>
실험 결과, 예시가 지나치게 많으면 오히려 System Prompt의 핵심 지시 사항이 희석되는 현상이 관찰되어 개수를 제한했습니다. 아울러, 단순 질의응답(Single Turn) 형태보다 사고의 흐름을 보여주는 **Multi-turn 대화 형식**의 예시가 모델 성능 향상에 더 효과적임을 확인하고 이를 적용했습니다.

**3) Temperature** <Br>
실험 결과의 일관된 비교 분석을 위해 **Temperature를 0으로 설정**했습니다. <br>
이를 통해 무작위성을 배제하고 결정론적(Deterministic)인 결과를 산출함으로써, 프롬프트 변화에 따른 성능 차이를 명확하게 측정할 수 있도록 통제했습니다




