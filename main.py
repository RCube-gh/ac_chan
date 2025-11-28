import argparse
from scrape import scrape_contest
from login import login


def main():
    parser=argparse.ArgumentParser(prog="acchan")
    subparsers=parser.add_subparsers(dest="command")

    gen_parser=subparsers.add_parser("gen")
    gen_parser.add_argument("contest_id",type=str,help="Contest ID (e.g., abc123)")

    login_parser=subparsers.add_parser("login")

    args=parser.parse_args()

    if args.command=="gen":
        scrape_contest(args.contest_id)
    elif args.command=="login":
        login()
    else:
        parser.print_help()


if __name__=="__main__":
    main()
