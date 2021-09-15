# flake8: noqa W191
from vv.frontend_models.model import FrontendModel

from introspection.model import ModelRepresentation

from .base import VvBaseTest


class VVTestConf(VvBaseTest):
    def test_frontend_model_base(self):
        model = ModelRepresentation("testapp", "Instrument")
        fm = FrontendModel(model)
        val = 'import InstrumentContract from "./contract"'
        self.assertEqual(fm.contract_import, val)
        val = 'import api from "../../api"'
        self.assertEqual(fm.api_relative_import, val)
        self.assertEqual(fm.snake_case_name, "instrument")

    def test_frontend_model_load_method(self):
        model = ModelRepresentation("testapp", "Instrument")
        fm = FrontendModel(model)
        val = """	static async load(id: number | string): Promise<Instrument> {
		const res = await api.get<Record<string, any>>(`/api/instrument/${id}/`);
		return Instrument.fromJson(res)
	}"""
        self.assertEqual(val, fm.load_method())

    def test_frontend_model_tsclass(self):
        model = ModelRepresentation("testapp", "Instrument")
        fm = FrontendModel(model)
        val = """import InstrumentContract from "./contract";

export default class Instrument {
	id: number;
	name: string;

	constructor ({ id, name }: InstrumentContract) {
		this.id = id;
		this.name = name
	}

	static fromJson(data: Record<string, any>): Instrument {
		return new Instrument(data as InstrumentContract)
	}
}"""
        self.assertEqual(fm.tsclass(), val)

    def test_frontend_model_tsclass_with_relation(self):
        model = ModelRepresentation("testapp", "Market")
        fm = FrontendModel(model)
        val = """import AgentContract from "../agent/contract";
import MarketContract from "./contract";

export default class Market {
	id: number;
	name: string;
	maker: AgentContract | null;
	agents: Array<AgentContract>;

	constructor ({ id, name, maker, agents }: MarketContract) {
		this.id = id;
		this.name = name;
		this.maker = maker;
		this.agents = agents
	}

	static fromJson(data: Record<string, any>): Market {
		return new Market(data as MarketContract)
	}
}"""
        self.assertEqual(fm.tsclass(), val)

    def test_frontend_model_contructor(self):
        model = ModelRepresentation("testapp", "Instrument")
        fm = FrontendModel(model)
        val = """	constructor ({ id, name }: InstrumentContract) {
		this.id = id;
		this.name = name
	}"""
        self.assertEqual(val, fm.constructor())

    def test_frontend_model_interface(self):
        model = ModelRepresentation("testapp", "Instrument")
        fm = FrontendModel(model)
        val = """export default interface InstrumentContract {
	id: number,
	name: string,
}"""
        self.assertEqual(val, fm.interface())

    def test_frontend_model_interface_with_relation(self):
        model = ModelRepresentation("testapp", "Market")
        fm = FrontendModel(model)
        val = """import AgentContract from "../agent/contract";

export default interface MarketContract {
	id: number,
	name: string,
	maker: AgentContract | null,
	agents: Array<AgentContract>,
}"""
        self.assertEqual(val, fm.interface())
