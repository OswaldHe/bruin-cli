import argparse
from bruin.meal import print_menu_all

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("option", type=str, help=
    "Tools that can be used in this cli, including:\n\n\
meal: print today's menu for each dining hall."
)

def main():
    args = parser.parse_args()
    if args.option == "meal":
        print_menu_all()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()