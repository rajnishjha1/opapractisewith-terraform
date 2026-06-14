import json
import re
from pathlib import Path

from bedrock_client import invoke_claude

ROOT = Path("../terraform")

PROMPT_FILE = Path(
    "prompts/terraform_review.txt"
)

REPORT_DIR = Path("../reports")

REPORT_DIR.mkdir(
    exist_ok=True
)

def load_terraform_code():

    tf_code = ""

    for file in ROOT.glob("*.tf"):

        tf_code += f"\n\n### FILE: {file.name}\n"

        tf_code += file.read_text()

    return tf_code


def load_prompt(terraform_code):

    prompt_template = PROMPT_FILE.read_text()

    return prompt_template.replace(
        "{{terraform_code}}",
        terraform_code
    )


def extract_json(response):

    match = re.search(
        r"\{.*\}",
        response,
        re.DOTALL
    )

    if not match:
        raise Exception(
            "No JSON found in model output"
        )

    return json.loads(
        match.group()
    )


def save_report(report):

    output_file = REPORT_DIR / "ai-report.json"

    with open(
        output_file,
        "w"
    ) as f:

        json.dump(
            report,
            f,
            indent=4
        )


def print_summary(report):

    print("\n")
    print("=" * 60)
    print("AI GOVERNANCE REPORT")
    print("=" * 60)

    print(
        f"Risk Score: "
        f"{report.get('risk_score')}"
    )

    print("\nSecurity Findings:")

    for item in report.get(
        "security",
        []
    ):
        print(f"- {item}")

    print("\nRecommendations:")

    for item in report.get(
        "recommendations",
        []
    ):
        print(f"- {item}")

    print("=" * 60)


def main():

    terraform_code = load_terraform_code()

    prompt = load_prompt(
        terraform_code
    )

    print(
        "Sending Terraform to Bedrock..."
    )

    response = invoke_claude(
        prompt
    )

    report = extract_json(
        response
    )

    save_report(report)

    print_summary(report)

    risk_score = report.get(
        "risk_score",
        0
    )

    if risk_score >= 8:

        print(
            "\nHigh Risk Infrastructure"
        )

        exit(1)

    print(
        "\nAI Review Passed"
    )


if __name__ == "__main__":
    main()