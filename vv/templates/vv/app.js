{% load vv_tags %}

{% for appname, parts in apps.items %}
	{% include parts.components %}
{% endfor %}

var debug = {% if isdebug == True %}true{% else %}false{% endif %};

const app = new Vue({
	el: '#app',
    data () {
        return {
			{% for appname, parts in apps.items %}
				{% include parts.data %}
			{% endfor %}
			active: [],
        }
	},
	methods: {
		flush: function(preserve) {
			if (debug === true) {console.log("FLUSH")};
			for (i=0;i<this.active.length;i++) {
				v = app[this.active[i]];
				if (debug === true) {console.log("Preserve: "+this.active[i]+" / "+preserve)};
				if (this.active[i] != preserve) {
					if (debug === true) { console.log("flushing "+this.active[i])};
					var t = typeOf(v);
					if (debug === true) { console.log("TYPE "+t);};
					if (t === "string") {
						if (debug === true) { console.log(this.active[i]+ " -> Flushing string")};
						app[this.active[i]] = ""
					} else if (t === "array") {
						if (debug === true) { console.log(this.active[i]+ " -> Flushing array")};
						app[this.active[i]] = [];
					} else if (t === "object") {
						if (debug === true) { console.log(this.active[i]+ " -> Flushing object")};
						app[this.active[i]] = {}
					} else if (t === "boolean") {
						if (debug === true) { console.log(this.active[i]+ " -> Flushing boolean")};
						app[this.active[i]] = false
					}
					delete(this.active[i]);
				} else {
					if (debug === true) { console.log("Preserving "+this.active[i])};
				}
			}
			if (debug === true) { console.log("After flush active: "+this.active)};
		},
		isActive: function(item) {
			if (this.active.indexOf(item) > -1) {
				return true
			}
			return false
		},
		activate: function(args) {
			if (debug === true) { console.log("ACTIVATE "+args)};
			this.active = args;
			if (debug === true) { console.log("After activate active: "+this.active)};
		},
		pushActivate: function(args) {
			if (debug === true) { console.log("ACTIVATE "+args)};
			i = 0;
			while (i<args.length) {
				this.active.push(args[i]);
				i++
			}
			if (debug === true) { console.log("After activate active: "+this.active)};
		},
		loadData: function(resturl, action) {
			promise.get(resturl).then(function(error, data, xhr) {
			    if (error) {console.log('Error ' + xhr.status);return;}    
			    var parsed_data = JSON.parse(data);
			    action(parsed_data);
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
	{% include parts.routes %}
{% endfor %}
page()

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
	         var cookie = jQuery.trim(cookies[i]);
	       // Does this cookie string begin with the name we want?
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
{% for appname, parts in apps.items %}
	{% include parts.extra %}
{% endfor %}
