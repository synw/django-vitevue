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
			if (vvDebug === true) {console.log("FLUSH")};
			for (i=0;i<this.active.length;i++) {
				v = app[this.active[i]];
				if (vvDebug === true) {console.log("Preserve: "+this.active[i]+" / "+preserve)};
				if (this.active[i] != preserve) {
					if (vvDebug === true) { console.log("flushing "+this.active[i])};
					var t = typeOf(v);
					if (vvDebug === true) { console.log("TYPE "+t);};
					if (t === "string") {
						if (vvDebug === true) { console.log(this.active[i]+ " -> Flushing string")};
						app[this.active[i]] = ""
					} else if (t === "array") {
						if (vvDebug === true) { console.log(this.active[i]+ " -> Flushing array")};
						app[this.active[i]] = [];
					} else if (t === "object") {
						if (vvDebug === true) { console.log(this.active[i]+ " -> Flushing object")};
						app[this.active[i]] = {}
					} else if (t === "boolean") {
						if (vvDebug === true) { console.log(this.active[i]+ " -> Flushing boolean")};
						app[this.active[i]] = false
					}
					delete(this.active[i]);
				} else {
					if (vvDebug === true) { console.log("Preserving "+this.active[i])};
				}
			}
			if (vvDebug === true) { console.log("After flush active: "+this.active)};
		},
		isActive: function(item) {
			if (this.active.indexOf(item) > -1) {
				return true
			}
			return false
		},
		activate: function(args) {
			if (vvDebug === true) { console.log("ACTIVATE "+args)};
			this.active = args;
			if (vvDebug === true) { console.log("After activate active: "+this.active)};
		},
		pushActivate: function(args) {
			if (vvDebug === true) { console.log("ACTIVATE "+args)};
			i = 0;
			while (i<args.length) {
				this.active.push(args[i]);
				i++
			}
			if (vvDebug === true) { console.log("After activate active: "+this.active)};
		},
		loadData: function(resturl, action, error) {
			axios.get(resturl).then(function (response) {
				var parsed_data = JSON.parse(response.data);
			    action(parsed_data);
			}).catch(function (error) {
				console.log(error);
			});
		},
		loadRawData: function(resturl, action, error) {
			axios.get(resturl).then(function (response) {
			    action(response.data);
			}).catch(function (error) {
				console.log(error);
			});
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
		postForm: function(url, data, action, error) {
			var ax = axios.create({headers: {'X-CSRFToken': csrftoken}});
			ax({
				method: 'post',
				url: url,
				data: data,
			}).then(function (response) {
				action(response)
			}).catch(function (error) {
				error(error);
			});
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
{% if "vvcatalog"|is_installed %}
app.InitCatalog();
{% endif %}

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
}/*
$.ajaxSetup({
	scriptCharset: "utf-8",
	contentType: "application/json; charset=utf-8",
    crossDomain: false,
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
*/
{% for appname, parts in apps.items %}
	{% include parts.extra %}
{% endfor %}
