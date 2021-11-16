import json
from typing import Dict, List, Set, Tuple
from pathlib import Path
from vv.conf.models import VVAppConf, VVConf

from vv.utils import rel_path


def vite_conf_file(path: Path) -> Path:
    """
    Get a Vite config file from a path
    """
    jsconf = path / "vite.config.js"
    tsconf = path / "vite.config.ts"
    if jsconf.exists():
        print("Found a frontend/vite.config.js file")
        return jsconf
    if tsconf.exists():
        print("Found a frontend/vite.config.ts file")
        return tsconf
    raise ValueError(f"No Vite config file found for path {path}")


def rel_app_dirs(conf: VVConf, app: VVAppConf) -> Tuple[Path, Path, Path]:
    """
    Get an app's compilation output dirs
    """
    # print("Base dir:", conf.base_dir)
    rel_app_dir = rel_path(app.directory, conf.vv_base_dir)
    rel_static_dir = rel_path(app.static, app.directory)
    rel_template = rel_path(app.template, app.directory)
    # print("Base dir", conf.base_dir)
    # print("Static dir", app.static, rel_static_dir)
    return (rel_app_dir, rel_static_dir, rel_template)


def generate_vite_compilation_config(
    conf: VVConf, app: VVAppConf, is_partial: bool = False
) -> str:
    """
    Configure Vitejs compilation output dir
    """
    print(f"Configuring app {app.directory.name} with these compilation destinations:")
    rel_app_dir, rel_static_dir, rel_template = rel_app_dirs(conf, app)
    print("static assets -> ", rel_static_dir)
    print("template -> ", rel_template)
    # buf: List[str] = []
    buf: List[str] = [f'\tpublicDir: "{rel_static_dir}",']
    buf.append("\tbuild: {")
    buf.append("\t\temptyOutDir: false,")
    buf.append("\t\trollupOptions: {")
    buf.append("\t\t\toutput: {")
    buf.append(f'\t\t\t\tdir: "{rel_static_dir}"')
    # app_name = app_dir.name
    # buf.append(f'\t\t\tchunkFileNames: "{app_name}/[name]-[hash].js"')
    # buf.append(f'\t\t\tentryFileNames: "{app_name}/[name].js"')
    # buf.append(f'\t\t\tassetFileNames: "{app_name}/[name]-[hash][extname]"')
    if is_partial is True:
        buf.append("\t\t\t},")
        buf.append("\t\t\tinput: {")
        buf.append(f'\t\t\t\tapp: "{app.template.relative_to(conf.templates_dir)}"')
        buf.append("\t\t\t}")
    else:
        buf.append("\t\t\t}")
    buf.append("\t\t}")
    buf.append("\t}")
    return "\n".join(buf)


def write_conf(app_dir: Path, viteconf: str, verbose: bool = True) -> None:
    """
    Write the Vite conf for an app
    """
    filename = vite_conf_file(app_dir)
    if verbose is True:
        print(f"Writing config in {filename.name}")
    lines = open(filename, "r").readlines()
    new_pre_last_line = lines[-2].rstrip()
    if not new_pre_last_line.endswith(","):
        new_pre_last_line = new_pre_last_line + ","
    new_pre_last_line = new_pre_last_line + "\n"
    new_last_line = lines[-1].rstrip().replace("})", viteconf + "\n})")
    lines[-2] = new_pre_last_line
    lines[-1] = new_last_line
    open(filename, "w").writelines(lines)


def generate_packages_json_build_commands(
    conf: VVConf, app: VVAppConf
) -> Dict[str, str]:
    """
    Generate the package.json commands for the build
    """
    rel_app_dir, rel_static_dir, rel_template = rel_app_dirs(conf, app)
    buf: Dict[str, str] = {
        "build:prepare": f"del {rel_static_dir}/assets/* {rel_template} --force"
    }
    buf["build:build"] = f"vite build --base={conf.static_url}{rel_app_dir.name}/"
    buf[
        "build:moveindex"
    ] = f"move-file {rel_static_dir}/{rel_template.name} {rel_template}"
    buf["build:clean"] = "del ./dist"
    buf["build"] = "run-s build::prepare build::build build::moveindex build:clean"
    return buf


def packages_conf(
    packages_conf_path: Path, cmds: Dict[str, str], read_only: bool = False
) -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Write the packages.json config file and return the list
    of packages dependencies and dev dependencies found
    """
    deps: Dict[str, str] = {}
    dev_deps: Dict[str, str] = {}
    with open(packages_conf_path, "r+") as jsonFile:
        data = json.load(jsonFile)
        # print(data["scripts"])
        # print("CMDS", cmds)
        deps = data["dependencies"]
        dev_deps = data["devDependencies"]
        for cmd in cmds:
            data["scripts"][cmd] = cmds[cmd]
        if not read_only:
            jsonFile.seek(0)
            json.dump(data, jsonFile, indent=4)
            jsonFile.truncate()
    return deps, dev_deps


def check_packages_dependencies(packages: Dict[str, str]):
    """
    Check if the npm dependencies required for compilation
    are installed in package.json
    """
    required: Set[str] = {"del-cli", "npm-run-all", "move-file-cli"}
    if not required.issubset(packages):
        print("Some npm dev dependencies are missing and require to be installed:")
        missing: Set[str] = set()
        for req in required:
            if not {req}.issubset(packages):
                missing.add(req)
        line = " ".join(missing)
        print(f"yarn add -D {line}")
        print("# or")
        print(f"npm install {line} --save-dev")
