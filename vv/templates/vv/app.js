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
	},
	methods: {
		{% for appname, parts in apps.items %}
			{% include parts.methods %}
		{% endfor %}
		flushContent: function() {
			app.content = "";
			{% if "vvcatalog"|is_installed %}
				this.products = [];
				this.categories = [];
			{% endif %}
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
