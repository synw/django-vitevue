{% load vv_tags %}

{% for appname, parts in apps.items %}
	{% include parts.components %}
{% endfor %}
	
const app = new Vue({
	el: '#app',
	data: {
		{% for appname, parts in apps.items %}
			{% include parts.data %}
		{% endfor %}
		active: []
	},
	methods: {
		{% for appname, parts in apps.items %}
			{% include parts.methods %}
		{% endfor %}
		flush: function() {
			//console.log("FLUSH");
			for (i=0;i<this.active.length;i++) {
				v = app[this.active[i]];
				//console.log("flushing "+this.active[i])
				var t = typeOf(v);
				if (t === "string") {
					app[this.active[i]] = ""
				} else if (t === "array") {
					app[this.active[i]] = [];
				} else if (t === "object") {
					app[this.active[i]] = {}
				}
				this.active.pop(v);
			}
		},
		activate: function(args) {
			//console.log("ACTIVATE "+args);
			this.active = args;
		},
		loadData: function(resturl, action) {
			promise.get(resturl).then(function(error, data, xhr) {
			    if (error) {console.log('Error ' + xhr.status);return;}    
			    var parsed_data = JSON.parse(data);
			    action(parsed_data);
			});
		}
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
