# Django Vite Vue

Manage a Vue.js frontend from several Django modules. Uses [Vue.js](http://vuejs.org/) for data binding,
 [Page.js](https://github.com/visionmedia/page.js) for client-side routing and [Axios](https://github.com/mzabriskie/axios)
 for fetching data.

For install and usage instructions read the [documentation](http://vite-vue.readthedocs.io/en/latest/)

## Quick examples

### Fetch content

In `your_module/templates/vue/data.js`:

  ```javascript
content: "",
  ```

In a template:

  ```html
<div v-html="content" v-show="isActive('content')"></div>
  ```

In `your_module/templates/vue/methods.js`:

  ```javascript
loadMyContent: function(url) {
	function error(err) {
		console.log(err)
	}
	function action(data) {
		// update UI
		app.content = data.somejsonkey;
		// manage state
		app.activate(["content"]);
	}
	this.loadData(url, action, error);
},
  ```

### Post a form

In `yourmodule/templates/yourmodule/yourmodel_form.html`:

  ```html
<form id="formid" onsubmit="return false" method="post">
    {% csrf_token %}
    {{ form }}
    <button class="button" onclick="javascript:app.postMyForm()">Save</button>
</form>
  ```

In `your_module/templates/vue/methods.js`

  ```javascript
postMyForm: function() {
	function error(err) {
		console.log(err)
	}
	function action(response) {
		if (response.data.error === 0) {
			app.notify("Ok", "content", 5, "success");
		} else {
			app.notify("Error", "content", 5, "danger");
		}
	}
	var url = "/myapp/add";
	this.postForm(url, "formid", action, error);
},
  ```
  
In `yourmodule/views.py`:

  ```python
# -*- coding: utf-8 -*-
from vv.views import PostFormView
from .models import MyModel


class MyModelCreate(PostFormView):
	model = MyModel
	fields = ['field1", "field2"]

	def action(self, request, clean_data):
		MyModel.objects.save(field1=clean_data["field1"], field2=clean_data["field2"])
  ```

## Client side routing

Optionaly set a client side route in `your_module/templates/routes.js`:

  ```javascript
page('/mycontent/', function(ctx, next) { app.loadContent("{% url 'myurl' %}") });
  ```

The `loadContent` method will then be triggered by the link `<a href="/mycontent/">load content</a>`

## What is that name?

In french language "vue" means view, "vite" means quick. The popular expression "Vite vu" means something quickly
done or evaluated. As this module is based on Vue.js and helps making the things done pretty quick it sounded appropriate
to call it Vite Vue. 
