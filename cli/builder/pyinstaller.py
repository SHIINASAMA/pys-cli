def build_pyinstaller_cmd(args):
    workpath = 'build/' + ('pyinstaller_onefile_build' if args.onefile else 'pyinstaller_onedir_build')
    cmd = [
        'pyinstaller',
        '--onefile' if args.onefile else '--onedir',
        '--distpath', 'build',
        '--workpath', workpath,
        '--noconfirm',
        '--log-level', 'DEBUG' if args.debug else 'WARN',
        '--name', 'App', 'app/__main__.py',
    ]
    cmd.extend(args.backend_args)
    return cmd