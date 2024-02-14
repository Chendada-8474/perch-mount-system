import flask


def key_generate() -> str:
    args = flask.request.args
    return phrase_key(args)


def phrase_key(args: dict) -> str:
    args_list = [f"{k}={v}" for k, v in args.items()]
    args_list.sort()
    return "&".join(args_list)
