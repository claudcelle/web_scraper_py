import sys

def main():
    print("Hello from web-scaper-py!")

    args = sys.argv
    if len(args)<2:
        print("no website provided")
        sys.exit(1)
    if len(args)>2:
        print("too many arguments provided")
        sys.exit(1)
    BASE_URL=args[1]
    print(f"starting crawl of: {BASE_URL}")
    


if __name__ == "__main__":
    main()
