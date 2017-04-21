{% load vv_tags %}
var vvDebug = {% isdebug %};
const app = new Vue({
	el: '#app',
    data () {
        return {
			{% for appname, parts in apps.items %}
				{% include parts.data %}
			{% endfor %}
			active: [],
			showSidebar: false,
			mainCol: {
				"col-xs-12": true,
				'col-sm-8': false,
				'col-sm-pull-4': false
			},
			sideCol: {
				"col-xs-12": true,
				'col-sm-4': false,
				'col-sm-push-8': false,
				"hidden": true
			},
        }
	},
	methods: {
		flush: function(preserve) {
			if (vvDebug === true) {console.log("FLUSH"+"\n# active: "+this.active, this.active.length)};
			var act = [];
			for (i=0;i<this.active.length;i++) {
				if (vvDebug === true) {if (preserve) {console.log("Preserve: "+this.active[i]+" / "+preserve)}};
				if (this.active[i] != preserve) {
					var t = typeOf(this.active[i]);
					if (isNaN(t)) {
						if (vvDebug === true) { console.log("NaN value "+this.active[i])};
						continue
					}
					if (t === "string") {
						if (vvDebug === true) { console.log(+ " [x] Flushing "+this.active[i]+" (string)")};
						this.active[i] = "";
					} else if (t === "array") {
						if (vvDebug === true) { console.log(+ " [x] Flushing "+this.active[i]+" (array)")};
						this.active[i] = [];
					} else if (t === "object") {
						if (vvDebug === true) { console.log(+ " [x] Flushing "+this.active[i]+" (object)")};
						this.active[i] = {}
					} else if (t === "boolean") {
						if (vvDebug === true) { console.log(+ " [x] Flushing "+this.active[i]+" (boolean)")};
						this.active[i] = false
					} else if (t === "number") {
						if (vvDebug === true) { console.log(+ " [x] Flushing "+this.active[i]+" (number)")};
						this.active[i] = 0
					} else {
						if (vvDebug === true) { console.log("Type not found "+this.active[i])};
						continue
					}
					act.push(this.active[i]);
				} else {
					if (vvDebug === true) { console.log("Preserving "+this.active[i])};
				}
			}
			this.active = act;
			if (vvDebug === true) { console.log("--> active: "+this.active+"\n ****** flushed *****\n") };
		},
		isActive: function(item) {
			if (this.active.indexOf(item) > -1) {
				return true
			}
			return false
		},
		activate: function(args) {
			if (vvDebug === true) { 
				console.log("ACTIVATE "+args);
				console.log("# active: "+this.active);
			};
			for (i=0;i<args.length;i++) {
				this.active.push(args[i]);
			}
			if (vvDebug === true) { console.log("--> active: "+this.active+"\n ****** activated *****\n")};
		},
		deactivate: function(args) {
			if (vvDebug === true) { 
				console.log("#### DEACTIVATE "+args);
				console.log("# active: "+this.active);
			};
			for (i=0;i<args.length;i++) {
				if (this.isActive(args[i])) {
					if (vvDebug === true) { console.log("[x] deactivating "+args[i]) };
					var index = this.active.indexOf(args[i]);
					this.active.splice(index, 1);
				}
			}
			if (vvDebug === true) { console.log("--> active: "+this.active+"\n #### deactivated\n")};
		},
		loadData: function(resturl, action, error) {
			axios.get(resturl).then(function (response) {
			    action(response.data);
			}).catch(function (error) {
				console.log(error);
			});
		},
		loadContent: function(resturl, title) {
			function action(data) {
				document.title = title;
				app.flush();
				app.pageContent = data;
				app.activate(['pageContent']);
			}
			function error(err) {
				console.log(err);
			}
			this.loadData(resturl, action, error);
		},
		toggleSidebar: function() {
			if ( this.showSidebar === false ) {
				this.mainCol = {
					"col-xs-12": true,
					'col-sm-8': true,
					'col-sm-pull-4': true
				},
				this.sideCol = {
					"col-xs-12": true,
					'col-sm-4': true,
					'col-sm-push-8': true,
					"hidden": false
				}
				this.showSidebar = true;
			} else {
				this.mainCol = {
					"col-xs-12": true,
					'col-sm-8': false,
					'col-sm-pull-4': false
				},
				this.sideCol = {
					"col-xs-12": true,
					'col-sm-4': false,
					'col-sm-push-8': false,
					"hidden": true
				}
				this.showSidebar = false;
			}
		},
		str: function(el) {
			return JSON.stringify(el, null, 2)
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
		{% for appname, parts in apps.items %}
			{% include parts.methods %}
		{% endfor %}
	},
	computed: {
		{% for appname, parts in apps.items %}
			{% include parts.computed %}
		{% endfor %}
	},
});
{% for appname, parts in apps.items %}
	{% if appname != "vvpages" %}
		{% include parts.routes %}
	{% endif %}
{% endfor %}
{% if "vvpages"|is_installed %}
	{% include "vvpages/routes.js" %}
{% endif %}
page();
function typeOf (obj) {
  return {}.toString.call(obj).split(' ')[1].slice(0, -1).toLowerCase();
}
function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
{% for appname, parts in apps.items %}
	{% include parts.extra %}
{% endfor %}
