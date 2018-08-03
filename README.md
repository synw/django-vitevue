# Django Vite Vue

Manage a Vue.js frontend from several Django modules. Uses [Vue.js](http://vuejs.org/) for data binding,
 [Page.js](https://github.com/visionmedia/page.js) for client-side routing and [Axios](https://github.com/mzabriskie/axios)
 for fetching data.

For install and usage instructions read the [documentation](http://vite-vue.readthedocs.io/en/latest/)

## Quick example

Fetch content and display it:

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
postMyForm: function() {
	function error(err) {
		console.log(err)
	}
	function action(response) {
		console.log(response.data)
	}
	var form = document.getElementById("myform");
	var data = this.serializeForm(form);
	this.postForm(url, data, action, error)
},
  ```
  
Declare your app in `settings.py` so that your frontend parts will be assembled: `VV_APPS = ["myapp"]`

Optionaly set a client side route in `your_module/templates/routes.js`:

  ```javascript
page('/mycontent/', function(ctx, next) { app.loadContent("{% url 'myurl' %}") });
  ```

The `loadContent` method will then be triggered by the link `<a href="/mycontent/">load content</a>`

### What is that name?

In french language "vue" means view, "vite" means quick. The popular expression "Vite vu" means something quickly
done or evaluated. As this module is based on Vue.js and helps making the things done pretty quick it sounded appropriate
to call it Vite Vue. 
