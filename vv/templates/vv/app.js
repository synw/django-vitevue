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
