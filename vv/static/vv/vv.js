var vvDebug = false;

var vvMixin = {
	delimiters: ['{!', '!}'],
    data: function() {
        return {
        	active: [],
        };
    },
    methods: {
		isActive: function(item) {
			if (store.getters.active.indexOf(item) > -1) {
				return true
			}
			return false
		},
		isInactive: function(item) {
			if (store.getters.active.indexOf(item) === -1) {
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
		postForm: function(url, formname, action, error) {
			var form = this.get(formname);
			var data = this.serializeForm(form, true);
			if (data === false) {
				return
			};
			if ("csrfmiddlewaretoken" in data) {
				token = data.csrfmiddlewaretoken
			} else {
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
		serializeForm: function(form, validate) {
			var obj = {};
			var elements = form.querySelectorAll( "input, select, textarea" );
			for( var i = 0; i < elements.length; ++i ) {
				var element = elements[i];
				var name = element.name;
				var value = element.value;
				if (validate === true) {
					if (element.hasAttribute('required')) {
						if (!value) {
							if (vvDebug === true) { 
								console.log("Required field", name, "is missing. Not posting form.");
							}
							return false
						}
					}
				}
				if( name ) {
					obj[ name ] = value;
				}
			}
			return obj;
		},
		notify: function(txt, dest, delay, nclass) {
			delay = typeof delay !== 'undefined' ? delay : 5;
			var tdelay = delay*1000;
			nclass = typeof nclass !== 'undefined' ? nclass : "info";
			var html = '<div class="notification is-'+nclass+'">';
			html = html+'<button class="delete" onclick="javascript:app.closeNotif(\''+dest+'\')"></button>'+txt+'</div>';
			this[dest] = html;
			setTimeout(function(){app[dest] = ""}, tdelay);
		},
		closeNotif: function(dest) {
			this[dest] = "";
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