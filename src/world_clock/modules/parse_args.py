import argparse

def get_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="World Clock - Time zone converter and reporter")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # demo command
    subparsers.add_parser('demo', help='Show demonstration of all features')
    
    # now command
    now_parser = subparsers.add_parser('now', help='Show current time')
    now_parser.add_argument('--at', dest='timezone', help='Show current time at specific timezone')
    
    # from command
    from_parser = subparsers.add_parser('from', help='Convert time from one timezone to another')
    from_parser.add_argument('source', help='Source timezone or "local"')
    from_parser.add_argument('date', help='Date/time to convert')
    from_parser.add_argument('to', help='Target timezone or "local"')
    
    # diff command
    diff_parser = subparsers.add_parser('diff', help='Show time difference between timezones')
    diff_parser.add_argument('tz1', help='First timezone')
    diff_parser.add_argument('tz2', help='Second timezone')
    
    return parser.parse_args()