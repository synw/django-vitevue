const store = new Vuex.Store({
	state: {
		active: [],
    	pageTitle: "",
	},
	mutations: {
		activate: function(state, elems, push) {
			console.log("MUT * ACTIVATE", elems);
			if (push) {
				for (i=0;i<elems.length;i++) {
					console.log("EL", elems[i]);
					state.active.push(elems[i]);
				}
			} else {
				state.active = elems;
			}
			console.log("END", state.active);
		},
		deactivate: function(state, elems) {
			for (i=0;i<state.active.length;i++) {
				if (elems[i] === state.active[i]) {
					var index = state.active.indexOf(elems[i]);
					state.active.splice(index, 1);
				}
			}
		},
		setPageTitle: function(state, title) {
			state.pageTitle = title;
		},
		fillSidebar: function(state, content) {
			state.sidebar = content;
		},
	},
	actions: {
		activate: function(context, elems) {
			context.commit("activate", elems);
		},
		deactivate: function(context, elems) {
			context.commit("deactivate", elems);
		},
		setPageTitle: function(context, title) {
			context.commit("setPageTitle", title);
		},
		fillSidebar: function(context, content) {
			context.commit("fillSidebar", content);
		},
	},
	getters: {
		active: function(state) { return state.active },
    	pageTitle: function(state) { return state.pageTitle },
    	sidebar: function(state) { return state.sidebar },
	},
});