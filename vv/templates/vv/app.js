{% load vv_tags %}

{% for appname, parts in apps.items %}
	{% include parts.components %}
{% endfor %}

//var debug = {% if isdebug == True %}true{% else %}false{% endif %};
var debug = true;

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
		loadForm: function(resturl, id, title) {
			this.loadChunk(resturl, title);
			init_form(id, resturl);
		},
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

var forms = {};
{% for appname, parts in apps.items %}
	var fms = {% include parts.forms %};
	console.log("FMS {{ appname }} "+fms[i]);
	for (key in fms) {
		forms[key] = fms[key];
	}
{% endfor %}
if (debug === true) { console.log("FORMS "+JSON.stringify(forms))};

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
function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function post_form(frm, url, appv) {
	$.ajax({
	      type: 'POST',
	      url: url,
	      data: frm.serialize(),
	      dataType : 'html',
	      success: function (response) {
	    	  if (debug === true) {console.log(response)};
	          appv = response;
	      },
	      error: function(xhr, textStatus, error) {
	      	console.log("Error:");
	          console.log(xhr.statusText);
			    console.log(textStatus);
			    console.log(error);
	      }
	  });
}
var csrftoken = getCookie('csrftoken');
$.ajaxSetup({
 crossDomain: false,
 beforeSend: function(xhr, settings) {
     if (!csrfSafeMethod(settings.type)) {
         xhr.setRequestHeader("X-CSRFToken", csrftoken);
     }
 }
});
function init_form(key, url) {
	console.log("FORM "+key+" "+url);
	var frm = $(key);
	frm.submit(function (ev) {
		console.log("POSTING form "+key+" "+url);
		ev.preventDefault();
		ev.stopImmediatePropagation();
	  	post_form(frm, url);
	  	return false;
	});
}
