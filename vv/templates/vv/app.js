{% load vv_tags %}

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
	}
});

{% for appname, parts in apps.items %}
	{% include parts.routes %}
{% endfor %}
page()
