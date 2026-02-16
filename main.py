import argparse

from csvclean.cli import base_process


def main():
    parser = argparse.ArgumentParser(description="CSV Cleaner")

    parser.add_argument("--input", required=True, help="Csv path")
    parser.add_argument("--output", required=True, help="Output path of clean csv")
    parser.add_argument("--report", action="store_true", help="Show report")

    args = parser.parse_args()

    base_process(args.input, args.output, args.report)


if __name__ == "__main__":
    main()
