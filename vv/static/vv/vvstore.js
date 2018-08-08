const store = new Vuex.Store({
	state: {
		active: [],
	},
	mutations: {
		activate(state, elems) {
			for (i=0;i<elems.length;i++) {
				state.active.push(elems[i]);
			}
		},
		deactivate(state, elems) {
			for (i=0;i<elems.length;i++) {
				var index = state.active.indexOf(elems[i]);
				if (index > -1) {
					state.active.splice(index, 1);
				}
			}
		},
	},
	actions: {
		activate: function(context, elems) {
			context.commit("activate", elems);
		},
		deactivate: function(context, elems) {
			context.commit("deactivate", elems);
		},
	},
	getters: {
		active: function(state) { return state.active },
	},
});