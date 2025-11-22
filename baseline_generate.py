import os
import argparse

import pandas as pd
from tqdm import tqdm

# from dotenv import load_dotenv
from openai import OpenAI
from prompts import baseline_prompt

from prompt import (
    SYSTEM_PROMPT,
    USER_PROMPT,
)
from few_shot import construct_fewshot, TRAIN_DF, TOKENIZED_ORIGINAL_SENTENCES

# # Load environment variables
# load_dotenv()


def main():
    parser = argparse.ArgumentParser(
        description="Generate modified sentences using Upstage API"
    )
    parser.add_argument(
        "--input",
        default="data/test_dataset.csv",
        help="Input CSV path containing body_archaic_hangul column",
    )
    parser.add_argument("--output", default="submission.csv", help="Output CSV path")
    parser.add_argument(
        "--model", default="solar-pro2", help="Model name (default: solar-pro2)"
    )
    args = parser.parse_args()

    # Load data
    df = pd.read_csv(args.input)[300:]

    if "original_sentence" not in df.columns:
        raise ValueError("Input CSV must contain 'original_sentence' column")

    if "id" not in df.columns:
        raise ValueError("Input CSV must contain 'id' column")

    # Setup Upstage client
    # up_DcOODVGAn7Pw1j8JeLT6m3822OZcg
    api_key = dotenv
    if not api_key:
        raise ValueError("UPSTAGE_API_KEY not found in environment variables")

    client = OpenAI(api_key=api_key, base_url="https://api.upstage.ai/v1")

    print(f"Model: {args.model}")
    print(f"Output: {args.output}")

    ids = []
    original_sentence = []
    answer_sentence = []

    # Process each sentence
    for idx, text in enumerate(
        tqdm(df["original_sentence"].astype(str).tolist(), desc="Generating")
    ):
        ids.append(df.iloc[idx]["id"])  # Get id from original data
        original_sentence.append(text)

        few_shots = construct_fewshot(
            TRAIN_DF, TOKENIZED_ORIGINAL_SENTENCES, text, topk=5, chat_fewshot=True
        )

        resp1 = client.chat.completions.create(
            model=args.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *few_shots,
                {"role": "user", "content": USER_PROMPT.format(text=text)},
            ],
            temperature=0.0,
        )
        corrected = resp1.choices[0].message.content.strip()
        print(f"Draft:\n{corrected}\n")

        # resp2 = client.chat.completions.create(
        #     model=args.model,
        #     messages=[
        #         {
        #             "role": "system",
        #             "content": FEEDBACK_SYSTEM_PROMPT
        #         },
        #         {
        #             "role": "user",
        #             "content": FEEDBACK_USER_PROMPT.format(origin_text=text, draft_text=corrected)
        #         }
        #     ],
        #     temperature=0.0,
        # )
        # feedback = resp2.choices[0].message.content.strip()
        # # print(f"Feedback:\n{feedback}\n")

        # resp3 = client.chat.completions.create(
        #     model=args.model,
        #     messages=[
        #         {
        #             "role": "system",
        #             "content": FINAL_SYSTEM_PROMPT
        #         },
        #         {
        #             "role": "user",
        #             "content": FINAL_USER_PROMPT.format(origin_text=text, draft_text=corrected, feedback=feedback)
        #         }
        #     ],
        #     temperature=0.0,
        # )
        # final = resp3.choices[0].message.content.strip()
        # answer_sentence.append(final)

        # print(f"Final:\n{final}\n")
        answer_sentence.append(corrected)

        # print(f"Error processing: {text[:50]}... - {e}")
        # answer_sentence.append(text)  # fallback to original

    # Save results with required column names (including id)
    out_df = pd.DataFrame(
        {
            "id": ids,
            "original_sentence": original_sentence,
            "answer_sentence": answer_sentence,
        }
    )
    out_df.to_csv(args.output, index=False)
    print(f"Wrote {len(out_df)} rows to {args.output}")


if __name__ == "__main__":
    main()
