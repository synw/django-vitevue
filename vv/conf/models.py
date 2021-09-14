import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class VVAppConf:
    """
    A class to hold a vv app conf
    """

    # source directory
    directory: Path
    # compilation destination
    static: Path
    template: Path
    # compilation options
    is_partial: bool = field(default=False)


@dataclass
class VVConf:
    """A class to hold a vv conf"""

    # base settings paths
    base_dir: Path
    vv_base_dir: Path
    staticfiles_dir: Path
    templates_dir: Path
    static_url: str

    def to_json_str(self) -> str:
        """Generate an indented json string representation

        :return: indented json string
        :rtype: str
        """
        return json.dumps(asdict(self), indent=2, default=str)
