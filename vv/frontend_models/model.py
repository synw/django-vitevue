from __future__ import annotations
from typing import List

from introspection import ModelRepresentation, ModelFieldRepresentation

from ..utils import field_ts_type_from_classname, to_snake_case


class FrontendModel:
    model: ModelRepresentation

    def __init__(self, model: ModelRepresentation) -> None:
        """
        Initialize from a model representation
        """
        self.model = model

    @property
    def get_import(self) -> str:
        """
        Get the Typescript import for this model
        """
        return (
            f"import {self.model.name} from @/models/{to_snake_case(self.model.name)}"
        )

    @property
    def contract_import(self) -> str:
        """
        Get the Typescript contract import for this model
        """
        return (
            f"import {self.model.name}Contract from @/models/"
            f"{to_snake_case(self.model.name)}/contract"
        )

    def interface(self) -> str:
        """
        Get a Typescript interface for a model
        """
        buf: List[str] = []
        buf.append(f"export default interface {self.model.name}Contract " + "{")
        for field in self.model.fields:
            buf.append(self.field_type(field) + ",")
        buf.append("}")
        return "\n".join(buf)

    def constructor(self) -> str:
        """
        Get a Typescript constructor for a model
        """
        buf: List[str] = []
        params: List[str] = []
        main: List[str] = []
        for field in self.model.fields:
            main.append(f"\t\tself.{field.name}={field.name}")
            params.append(f"{field.name}")
        c_begin = "\tconstructor ({"
        c_end = f": {self.model.name}Contract) {'{'}"
        buf.append(c_begin + ", ".join(params) + "}" + c_end)
        buf.append(";\n".join(main))
        buf.append("\t}")
        return "\n".join(buf)

    def tsclass(self) -> str:
        """
        Render a Typescript class for a model
        """
        interface = self.contract_import
        buf: List[str] = [interface + ";\n"]
        buf.append(f"export default class {self.model.name} {'{'}")
        for field in self.model.fields:
            buf.append(self.field_type(field) + ";")
        buf.append(f"\n{self.constructor()}")
        buf.append("}")
        return "\n".join(buf)

    def field_type(self, field: ModelFieldRepresentation) -> str:
        """
        Get the typescript field type definition string
        """
        return f"\t{field.name}: {field_ts_type_from_classname(field.classname)}"
