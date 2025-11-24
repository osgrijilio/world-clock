from world_clock.modules import actions, parse_args

if __name__ == "__main__":

    args = parse_args.get_cli_args() 

    if not args.command or args.command == 'demo':
        actions.demo()
    elif args.command == 'now':
        if args.timezone:
            actions.report_now_at_timezone_name(args.timezone)
        else:
            actions.report_now()
    elif args.command == 'from':
        if args.source == 'local':
            actions.report_translate_date_to_tz(args.date, args.to)
        elif args.to == 'local':
            actions.report_translate_date_from_tz(args.date, args.source)
        else:
            actions.report_translate_date_between_tz(args.date, args.source, args.to)
    elif args.command == 'diff':
        actions.report_timezones_diff(args.tz1, args.tz2)
