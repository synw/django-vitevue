from vv.frontend_models.model import FrontendModel

from introspection.model import ModelRepresentation

from .base import VvBaseTest


class VVTestConf(VvBaseTest):
    def test_frontend_models(self):
        model = ModelRepresentation("testapp", "Instrument")
        fm = FrontendModel(model)
        print(fm)
        val = 'import InstrumentContract from "./contract"'
        self.assertEqual(fm.contract_import, val)
        val = 'import api from "../../api"'
        self.assertEqual(fm.api_relative_import, val)
        self.assertEqual(fm.snake_case_name, "instrument")
        """val = (
          f'import {relation_class_name}Contract from "../'
          f'{relation_model_name}/contract"')"""
