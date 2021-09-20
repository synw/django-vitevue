# from __future__ import annotations
from typing import List, Set

from introspection import ModelRepresentation, ModelFieldRepresentation

from ..utils import field_ts_type_from_classname, to_camel_case_var, to_snake_case


class FrontendModel:
    model: ModelRepresentation

    def __init__(self, model: ModelRepresentation) -> None:
        """Initialize from a model representation

        :param model: a model representation from django-introspection
        :type model: ModelRepresentation
        """
        self.model = model

    @property
    def contract_import(self) -> str:
        """Get the Typescript contract import for this model

        :return: a Typescript import string
        :rtype: str
        """
        return f'import {self.model.name}Contract from "./contract"'

    @property
    def api_relative_import(self) -> str:
        """Get the Typescript api import

        :return: a Typescript import string
        :rtype: str
        """
        return 'import api from "../../api"'

    @property
    def snake_case_name(self) -> str:
        """Convert the model name to snake case

        :return: the model name in snake case
        :rtype: str
        """
        return to_snake_case(self.model.name)

    def interface(self) -> str:
        """Get a Typescript interface for a model

        :return: the Typescript interface for the model
        :rtype: str
        """
        buf: List[str] = []
        extra_imports: Set[str] = set()
        buf.append(f"export default interface {self.model.name}Contract " + "{")
        for field in self.model.fields.values():
            buf.append(self.field_type(field) + ",")
            if field.is_relation is True:
                extra_imports.add(
                    self.relation_contract_import(
                        field.related_class_name,
                        to_snake_case(field.related_class_name),
                    )
                )
        buf.append("}")
        output = ""
        main = "\n".join(buf)
        if len(extra_imports) > 0:
            output = ";\n".join(extra_imports) + ";\n\n"
        output += main
        return output

    def constructor(self) -> str:
        """
        Get a Typescript constructor for a model
        """
        buf: List[str] = []
        params: List[str] = []
        main: List[str] = []
        for field in self.model.fields.values():
            main.append(f"\t\tthis.{field.name} = {field.name}")
            params.append(f"{field.name}")
        c_begin = "\tconstructor ({ "
        c_end = f": {self.model.name}Contract) {'{'}"
        buf.append(c_begin + ", ".join(params) + " }" + c_end)
        buf.append(";\n".join(main))
        buf.append("\t}")
        return "\n".join(buf)

    def tsclass(self) -> str:
        """
        Render a Typescript class for a model
        """
        interface = self.contract_import
        extra_imports: Set[str] = set()
        buf: List[str] = [interface + ";\n"]
        buf.append(f"export default class {self.model.name} {'{'}")
        for field in self.model.fields.values():
            buf.append(self.field_type(field) + ";")
            if field.is_relation is True:
                extra_imports.add(
                    self.relation_contract_import(
                        field.related_class_name,
                        to_snake_case(field.related_class_name),
                    )
                )
        buf.append(f"\n{self.constructor()}")
        buf.append("\n" + self.from_json_method())
        buf.append("}")
        output = ""
        if len(extra_imports) > 0:
            output = ";\n".join(extra_imports) + ";\n"
        output += "\n".join(buf)
        return output

    def from_json_method(self) -> str:
        """
        Get the to_json method for a Typescript class
        """
        buf: List[str] = [
            (
                f"\tstatic fromJson(data: Record<string, any>):"
                f" {self.model.name}"
                " {"
            )
        ]
        buf.append(
            f"\t\treturn new {self.model.name}(data as {self.model.name}Contract)"
        )
        buf.append("\t}")
        return "\n".join(buf)

    def load_method(self) -> str:
        """
        Get the load method for a Typescript class
        """
        buf: List[str] = [
            (
                f"\tstatic async load(id: number | string): Promise<{self.model.name}>"
                " {"
            )
        ]
        line = (
            "\t\tconst res = await api.get<Record<string, any>>(`/api/"
            f"{self.snake_case_name}/$"
            "{id}/`);"
        )
        buf.append(line)
        buf.append(f"\t\treturn {self.model.name}.fromJson(res)")
        buf.append("\t}")
        return "\n".join(buf)

    def field_type(self, field: ModelFieldRepresentation) -> str:
        """
        Get the typescript field type definition string
        """
        f = ""
        if field.is_relation is False:
            f = f"\t{field.name}: {field_ts_type_from_classname(field.classname)}"
        else:
            f = self.field_relation_type(field)
        return f

    def field_relation_type(self, field: ModelFieldRepresentation) -> str:
        """
        Get the typescript field type definition string
        for a relation field
        """
        val = f"{field.related_class_name}Contract"
        if field.classname == "ManyToManyField":
            val = f"Array<{field.related_class_name}Contract>"
        if field.is_null is True:
            val += " | null"
        return f"\t{to_camel_case_var(field.name)}: {val}"

    def relation_contract_import(
        self, relation_class_name: str, relation_model_name: str
    ) -> str:
        """
        Get an import line for a given model contract
        """
        return (
            f'import {relation_class_name}Contract from "../'
            f'{relation_model_name}/contract"'
        )
