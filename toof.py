import argparse


def main():
    parser = argparse.ArgumentParser(description="toof")
    parser.add_argument("input", help="input value")
    args = parser.parse_args()

    print(args.input)


if __name__ == "__main__":
    main()
