var vvDebug = false;

var vvMixin = {
    data: function() {
        return {
        	active: [],
        };
    },
    methods: {
    	flush: function(preserve) {
			if (vvDebug === true) {console.log("FLUSH"+"\n# active: "+store.getters.active, store.getters.active.length)};
			//var act = [];
			for (i=0;i<store.getters.active.length;i++) {
				if (vvDebug === true) {if (preserve) {console.log("Preserve: "+store.getters.active[i]+" / "+preserve)}};
				if (store.getters.active[i] != preserve) {
					var t = typeOf(store.getters.active[i]);
					if (t === "string") {
						if (vvDebug === true) { console.log(" [x] Flushing "+store.getters.active[i]+" (string)")};
						store.getters.active[i] = "";
					} else if (t === "array") {
						if (vvDebug === true) { console.log(" [x] Flushing "+store.getters.active[i]+" (array)")};
						store.getters.active[i] = [];
					} else if (t === "object") {
						if (vvDebug === true) { console.log(" [x] Flushing "+store.getters.active[i]+" (object)")};
						store.getters.active[i] = {}
					} else if (t === "boolean") {
						if (vvDebug === true) { console.log(" [x] Flushing "+store.getters.active[i]+" (boolean)")};
						store.getters.active[i] = false
					} else if (t === "number") {
						if (vvDebug === true) { console.log(" [x] Flushing "+store.getters.active[i]+" (number)")};
						store.getters.active[i] = 0
					} else {
						if (vvDebug === true) { console.log("Type not found "+store.getters.active[i])};
						continue
					}
					//act.push(store.getters.active[i]);
				} else {
					if (vvDebug === true) { console.log("Preserving "+store.getters.active[i])};
				}
			}
			//this.activate(act);
			//if (vvDebug === true) { console.log("--> active: "+store.getters.active+"\n ****** flushed *****\n") };
		},
		isActive: function(item) {
			if (store.getters.active.indexOf(item) > -1) {
				return true
			}
			return false
		},
		activate: function(args) {
			if (vvDebug === true) { 
				console.log("ACTIVATE "+args);
				console.log("# active: "+store.getters.active);
			};
			store.dispatch("activate", args)
			if (vvDebug === true) { console.log("--> active: "+store.getters.active+"\n ****** activated *****\n")};
		},
		deactivate: function(args) {
			if (vvDebug === true) { 
				console.log("#### DEACTIVATE "+args);
				console.log("# active: "+store.getters.active);
			};
			store.dispatch("deactivate", args)
			if (vvDebug === true) { console.log("--> active: "+store.getters.active+"\n #### deactivated\n")};
		},
		loadData: function(resturl, action, error) {
			axios.get(resturl).then(function (response) {
			    action(response.data);
			}).catch(function (error) {
				console.log(error);
			});
		},
		postForm: function(url, data, action, error, token) {
			if (!token) {
				token = csrftoken
			}
			var ax = axios.create({headers: {'X-CSRFToken': token}});
			ax({
				method: 'post',
				url: url,
				data: data,
			}).then(function (response) {
				action(response)
			}).catch(function (err) {
				error(err);
			});
		},
		serializeForm: function(form) {
			var obj = {};
			var elements = form.querySelectorAll( "input, select, textarea" );
			for( var i = 0; i < elements.length; ++i ) {
				var element = elements[i];
				var name = element.name;
				var value = element.value;
				if( name ) {
					obj[ name ] = value;
				}
			}
			return obj;
		},
		query: function(q) {
			var q = encodeURIComponent(q);
			var url = '/graphql?query='+q;
			return url
		},
		str: function(el) {
			return JSON.stringify(el, null, 2)
		},
		get: function(node) {
			return document.getElementById(node)
		},
    }
};