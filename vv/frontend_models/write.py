from pathlib import Path
from typing import Tuple

from django.core.management.base import CommandError

from .model import FrontendModel


def check_for_file_overwrite(file: Path, default_yes: bool = True) -> Tuple[bool, bool]:
    """
    Check if a file exists and prompt the user for overwrite
    """
    exists = False
    abort = False
    if file.exists() is True:
        abort = True
        exists = True
        resp: str
        if default_yes is True:
            resp = input(f"The file {file} already exists. Overwrite? [Y/n)")
            if resp in ["", "Y", "y", "yes"]:
                abort = False
        else:
            resp = input(f"The file {file} already exists. Overwrite? [y/N)")
            if resp in ["Y", "y", "yes"]:
                abort = False
    return abort, exists


def write_tsmodel(model: FrontendModel, destination_folder: Path, verbose=True):
    """
    Write a frontend Typescript model to a folder
    """
    if not destination_folder.exists():
        raise FileNotFoundError(f"Folder {destination_folder} not found")
    if verbose is True:
        print(f"Writing model {model.model.name}")
    # write constructor params interface
    contract = model.interface()
    filename = destination_folder / "contract.ts"
    # check if file exists
    abort, exists = check_for_file_overwrite(filename)
    if abort is True:
        raise CommandError("Aborting")
    if verbose is True:
        print(f"Writing contract in {filename}")
    mode = "x"
    if exists is True:
        mode = "w"
    with open(filename, mode) as f:
        f.write(contract)
    # write the model class
    tsclass = model.tsclass()
    filename = destination_folder / "index.ts"
    # check if file exists
    abort, exists = check_for_file_overwrite(filename)
    if abort is True:
        raise CommandError("Aborting")
    if verbose is True:
        print(f"Writing class {model.model.name} in {filename}")
    mode = "x"
    if exists is True:
        mode = "w"
    with open(filename, mode) as f:
        f.write(tsclass)
