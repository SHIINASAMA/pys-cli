import logging
import os
import sys

from cli.args import get_parser
from cli.builder.build import gen_version_py, build
from cli.builder.qt import build_i18n_ts, build_i18n, build_ui, build_assets, gen_init_py
from cli.cache import load_cache, save_cache
from cli.create import create
from cli.git import get_last_tag
from cli.glob import glob_files
from cli.pyproject import load_pyproject
from cli.pytest import run_test


def main():
    source_list = []
    ui_list = []
    asset_list = []
    i18n_list = []
    lang_list = []
    cache = {}
    extra_backend_options_list = []

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    args = get_parser().parse_args()
    if args.backend_args and args.backend_args[0] == "--":
        args.backend_args = args.backend_args[1:]

    if args.debug:
        logging.info('Debug mode enabled.')
        logging.getLogger().setLevel(logging.DEBUG)

    if args.create:
        create(args.create)
        sys.exit(0)

    # check working directory
    # if 'app' is not in the current working directory, exit
    if not os.path.exists('app'):
        logging.error('Please run this script from the project root directory.')
        sys.exit(1)

    if args.test:
        code = run_test(args)
        sys.exit(code)
    else:
        (asset_list,
         i18n_list,
         source_list,
         ui_list) = glob_files()

        (extra_backend_options_list, lang_list) = load_pyproject()

    if not args.no_cache:
        cache = load_cache()

    if args.i18n:
        build_i18n_ts(
            lang_list=lang_list,
            cache=cache,
            files_to_scan=[str(f) for f in ui_list + source_list]
        )
    if args.rc or args.all:
        build_ui(
            ui_list=ui_list,
            cache=cache
        )
        build_i18n(
            i18n_list=i18n_list,
            cache=cache
        )
        build_assets(
            asset_list=asset_list,
            cache=cache,
            no_cache=args.no_cache
        )
        gen_version_py(get_last_tag())
        gen_init_py()
    save_cache(cache)
    if args.build or args.all:
        build(args, extra_backend_options_list)


if __name__ == '__main__':
    main()
