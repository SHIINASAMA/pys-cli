import os


def build_nuitka_cmd(args, extra_nuitka_options_list):
    cmd = [
        'nuitka',
        '--output-dir=build',
        '--output-filename=App',
        'app',
        f'--jobs={os.cpu_count()}',
        '--onefile' if args.onefile else '--standalone'
    ]
    if args.debug:
        lt = [
            '--show-scons',
            '--verbose',
        ]
        cmd.extend(lt)
    cmd.extend(extra_nuitka_options_list)
    cmd.extend(args.backend_args)
    return cmd
