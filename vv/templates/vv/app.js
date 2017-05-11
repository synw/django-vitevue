{% load vv_tags %}
var vvDebug = {% isdebug %};
const app = new Vue({
	el: '#app',
	mixins: [vvMixin],
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
