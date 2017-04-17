# Django Vite Vue

Manage a Vue.js frontend from several Django modules. Uses [Vue.js](http://vuejs.org/) for data binding,
 [Page.js](https://github.com/visionmedia/page.js) for client-side routing and [Axios](https://github.com/mzabriskie/axios)
 for fetching data.

For install and usage instructions read the [documentation](http://vite-vue.readthedocs.io/en/latest/)

## Quick example

Fetch content and display it:

In `yourmodule_template_folder/vue/data.js`:

  ```javascript
content: "",
  ```

In a template:

  ```html
<div v-html="content" v-show="isActive('content')"></div>
  ```

In `yourmodule_template_folder/vue/methods.js`:

  ```javascript
loadContent: function(url) { 
	function action(data) {
		// update UI
		app.content = data.somejsonkey;
		// manage state
		app.flush();
		app.activate(["content"]);
	}
	this.loadData(url, action);
},
  ```
  
Declare your app in `settings.py` so that your frontend parts will be assembled: `VV_APPS = ["myapp"]`
  
Optionaly set a client side route in `yourmodule_template_folder/routes.js`:

  ```javascript
page('/mycontent/', function(ctx, next) { app.loadContent("{% url 'myurl' %}") });
  ```

The `loadContent` method will then be triggered by the link `<a href="/mycontent/">load content</a>`

