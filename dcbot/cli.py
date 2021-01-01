import inspect
import json
import argparse
from typing import Callable

from dcbot.dc import post


def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=lambda: parser.print_usage())
    subparsers = parser.add_subparsers()

    sp_post = subparsers.add_parser("post", help="post article")
    sp_post.add_argument("--dc-account", type=str, required=True, help="dcinside 계정")
    sp_post.add_argument("--dc-password", type=str, required=True, help="dcinside 계정 비밀번호")
    sp_post.add_argument("--gall-id", type=str, required=True, help="dcinside gall id(e.g. 미국주식: stockus)")
    sp_post.add_argument("--title", type=str, required=True, help="글 제목")
    sp_post.add_argument("--content", type=str, required=True, help="글 내용")
    sp_post.set_defaults(func=post)

    args = parser.parse_args()
    func = args.func
    run(func, args)


def run(func: Callable, args: argparse.Namespace):
    func_signature = inspect.signature(func)
    kwargs = {each_name: getattr(args, each_name) for each_name, each_parameter in func_signature.parameters.items()}
    output = func(**kwargs)
    if output is not None:
        print(json.dumps(output, indent=4))
