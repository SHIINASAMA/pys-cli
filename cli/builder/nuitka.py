import os


def build_nuitka_cmd(args, extra_nuitka_options_list):
    cmd = [
        'nuitka',
        '--output-dir=build',
        '--output-filename=App',
        'app/__main__.py',
        f'--jobs={os.cpu_count()}',
        '--onefile' if args.onefile else '--standalone'
    ]
    cmd.extend(extra_nuitka_options_list)
    cmd.extend(args.backend_args)
    return cmd
