Available methods
=================

State management
^^^^^^^^^^^^^^^^

A basic state management mechanism is used to manage the display. Methods:

``activate(["item1", "item2"])``: set active the given items. Usage:

.. highlight:: html

:: 

   <div v-show="isActive('myvariable')"></div>

``deactivate(["item1", "item2"])``: set inactive the given items

``isActive("item")``: return true or false

``isInactive("item")``: return true or false

``flush()``: reset all active items: all the active variables will be reseted: a string will be set to ``""``, 
a number to ``0``, an object to ``{}`` and a boolean to ``false``

To preserve an element from beeing flushed you can pass it to the function: ``flush("item")``
   

Fetch json data
^^^^^^^^^^^^^^^

``loadData(url, action, error)``: loads data and process actions on it

:: 

   function error(err) {
      console.log(err)
   }
   function action(data) {
      console.log(data)
   }
   this.loadData("{% url 'myurl' %}", action, error);
   
   
Post form
^^^^^^^^^

``postForm(url, formid, action, error)``: post a form

Note: the Django csrf token will be taken from the form if it is a Django form, otherwise it will be taken from
the session cookie

Ex: in ``mymodule/templates/vue/methods.js``:

.. highlight:: javascript

::

   postMyForm: function() {
      function error(err) {
         console.log(err)
      }
      function action(response) {
         console.log(response.data)
      }
      var url ="/myapp/add";
      this.postForm(url, "myform", action, error)
      // "myform" is the form id
   },
   
Notifications
^^^^^^^^^^^^^

``notify(txt, dest, delay, nclass)``: fills an app variable with a notification. Parameters: 

- ``txt``: the message 
- ``dest``: a string with the name of the destination app variable. 

Optional parameters: 

- ``delay``: the number of seconds that the notification will stay visible. Default is 5 seconds 
- ``nclass``: css class of the notification. Default is `info`

Example:

.. highlight:: javascript

::

   // lets say we have a variable named myvar in data.js
   app.notify("Ok", "myvar", 3, "success");
   // this will fill myvar with the notification html for 3 seconds with the success css class
   
Html output:

.. highlight:: html

::

   <div class="notification is-success">
      <button class="delete" onclick="javascript:app.closeNotif('myvar')"></button>
      Ok
   </div>
   
Note: the css is optimized for the Bulma css library

Shortcuts
^^^^^^^^^
   
``str(json_obj)``: shortcurt for pretty JSON.stringify

``get("id")``: shortcurt for document.getElementById

``query(querystring)``: shortcurt to encode a Graphql query: does '/graphql?query='+encodeURIComponent(querystring)


 