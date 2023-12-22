import argparse
import config


parser = argparse.ArgumentParser(description="Start the browser")

parser.add_argument('-n', '--no-proxy', action='store_true', default=False,
                    help='Disable default proxy')

parser.add_argument('--show-infobars', action='store_true', default=False,
                    help='Show infobars (disabled by default)')


def set_options(args: argparse.Namespace):
    if args.no_proxy:
        config.PROXY = None
    
    config.SHOW_INFOBARS = args.show_infobars
