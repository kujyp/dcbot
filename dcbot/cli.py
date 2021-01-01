import inspect
import json
import argparse
from typing import Callable

from dcbot.dc import post
from dcbot.tasks import fear_greed


def main():
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=lambda: parser.print_usage())
    subparsers = parser.add_subparsers()

    dc_parser = argparse.ArgumentParser(add_help=False)
    dc_parser.add_argument("--dc-nickname", type=str, required=True, help="dcinside 유동닉네임")
    dc_parser.add_argument("--dc-article-password", type=str, required=True, help="dcinside 작성글 비밀번호")
    dc_parser.add_argument("--gall-id", type=str, required=True, help="dcinside gall id(e.g. 미국주식: stockus)")

    sp_post = subparsers.add_parser("post", help="post article", parents=[dc_parser])
    sp_post.add_argument("--title", type=str, required=True, help="글 제목")
    sp_post.add_argument("--content", type=str, required=True, help="글 내용")
    sp_post.set_defaults(func=post)

    sp_post = subparsers.add_parser("fear", help="fear greed crawling and post article", parents=[dc_parser])
    sp_post.set_defaults(func=fear_greed)

    args = parser.parse_args()
    func = args.func
    run(func, args)


def run(func: Callable, args: argparse.Namespace):
    func_signature = inspect.signature(func)
    kwargs = {each_name: getattr(args, each_name) for each_name, each_parameter in func_signature.parameters.items()}
    output = func(**kwargs)
    if output is not None:
        print(json.dumps(output, indent=4))
