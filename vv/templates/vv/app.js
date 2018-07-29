{% load vv_tags %}
var vvDebug = {% isdebug %};
const app = new Vue({
	el: '#app',
	mixins: [vvMixin],
	delimiters: ['{!', '!}'],
    data () {
        return {
			{% for appname, parts in apps.items %}
				{% include parts.data %}
			{% endfor %}
        }
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
