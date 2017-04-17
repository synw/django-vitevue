# Django Vite Vue

Manage a Vue.js frontend from several Django modules. Uses [Vue.js](http://vuejs.org/) for data binding,
 [Page.js](https://github.com/visionmedia/page.js) for client-side routing and [Axios](https://github.com/mzabriskie/axios)
 for fetching data.

For install and usage instructions read the [documentation](http://vite-vue.readthedocs.io/en/latest/)

## Quick example

Fetch content and display it:

In `data.js`:

  ```javascript
content: "",
  ```

In `templates.js`:

  ```html
<div v-html="content" v-show="isActive('content')"></div>
  ```

In `methods.js`:

  ```javascript
function action(data) {
	// update UI
	app.content = data.somejsonkey;
	// manage state
	app.flush();
	app.activate(["content"]);
}
this.loadData("{% url 'myurl' %}", action);
  ```