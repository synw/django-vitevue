{% load vv_tags %}

{% for appname, parts in apps.items %}
	{% include parts.components %}
{% endfor %}
	
const app = new Vue({
	el: '#app',
    data () {
        return {
			{% for appname, parts in apps.items %}
				{% include parts.data %}
			{% endfor %}
			active: []
        }
	},
	methods: {
		{% for appname, parts in apps.items %}
			{% include parts.methods %}
		{% endfor %}
		flush: function(preserve) {
			//console.log("FLUSH");
			for (i=0;i<this.active.length;i++) {
				v = app[this.active[i]];
				//console.log("Preserve: "+this.active[i]+" / "+preserve);
				if (this.active[i] != preserve) {
					//console.log("flushing "+this.active[i])
					var t = typeOf(v);
					if (t === "string") {
						//console.log(this.active[i]+ " -> Flushing string");
						app[this.active[i]] = ""
					} else if (t === "array") {
						//console.log(this.active[i]+ " -> Flushing array");
						app[this.active[i]] = [];
					} else if (t === "object") {
						//console.log(this.active[i]+ " -> Flushing object");
						app[this.active[i]] = {}
					}
					delete(this.active[i]);
				} else {
					//console.log("Preserving "+this.active[i])
				}
			}
			//console.log("After flush active: "+this.active);
		},
		activate: function(args) {
			//console.log("ACTIVATE "+args);
			this.active = args;
			//console.log("After activate active: "+this.active);
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
	{% if "vvphotos"|is_installed %}
		components: {
	        'Slider': window[ 'vue-easy-slider' ].Slider,
	        'SliderItem': window[ 'vue-easy-slider' ].SliderItem
	      },
	{% endif %}
});

{% for appname, parts in apps.items %}
	{% include parts.routes %}
{% endfor %}
page()

function typeOf (obj) {
  return {}.toString.call(obj).split(' ')[1].slice(0, -1).toLowerCase();
}
