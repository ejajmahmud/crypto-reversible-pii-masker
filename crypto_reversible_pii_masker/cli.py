"""CLI for crypto-reversible-pii-masker."""
import sys
import argparse
from .masker import PIIMasker


def main():
    parser = argparse.ArgumentParser(description="Crypto Reversible PII Masker CLI")
    parser.add_argument("--demo", action="store_true", help="Run reversible PII masking demo")
    args = parser.parse_args()

    if args.demo:
        masker = PIIMasker()
        prompt = "Contact alice@example.com or bob@company.org regarding SSN 123-45-6789."
        m_res = masker.mask(prompt)

        print("Original Prompt:", prompt)
        print("Masked Prompt:  ", m_res.masked_text)

        # Simulate LLM output
        llm_output = f"I have notified <EMAIL_1> and verified the records for <SSN_1>."
        restored = masker.unmask(llm_output)
        print("Restored Output:", restored)
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
