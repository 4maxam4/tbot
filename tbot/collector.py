import sys
import importlib
import pathlib
import typing


def list_dir(d: pathlib.Path) -> typing.Generator[pathlib.Path, None, None]:
    for f in d.iterdir():
        if f.suffix == ".py":
            yield f


def get_file_list(
    dirs: typing.Iterable[pathlib.Path],
    files: typing.Iterable[pathlib.Path],
) -> typing.Generator[pathlib.Path, None, None]:
    tcpy = pathlib.Path.cwd() / "tc.py"
    if tcpy.is_file():
        yield tcpy

    tcdir = pathlib.Path.cwd() / "tc"
    if tcdir.is_dir():
        for f in list_dir(tcdir):
            yield f

    for d in dirs:
        if d.is_dir():
            for f in list_dir(d):
                yield f
        else:
            if d.exists():
                raise NotADirectoryError(str(d))
            else:
                raise FileNotFoundError(str(d))

    for f in files:
        if f.is_file():
            yield f
        else:
            raise FileNotFoundError(str(f))


def collect_testcases(
    files: typing.Iterable[pathlib.Path],
) -> typing.Dict[str, typing.Callable]:
    testcases: typing.Dict[str, typing.Callable] = {}

    default_sys_path = sys.path
    for f in files:
        try:
            module_spec = importlib.util.spec_from_file_location(
                name=f.stem,
                location=str(f),
            )
            module = importlib.util.module_from_spec(module_spec)
            if not isinstance(module_spec.loader, importlib.abc.Loader):
                raise TypeError(f"Invalid module spec {module_spec!r}")
            sys.path = default_sys_path + [str(f.parent)]
            module_spec.loader.exec_module(module)
        except:
            raise
        finally:
            sys.path = default_sys_path

        for name, func in module.__dict__.items():
            if hasattr(func, "_tbot_testcase"):
                if name in testcases:
                    raise KeyError(f"A testcase named {name!r} already exists: {func!r}")
                testcases[name] = func

    return testcases
