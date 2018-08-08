Available methods
=================

State management
^^^^^^^^^^^^^^^^

A basic state management mechanism is used to manage the display. Methods:

``flush()``: reset all active items: all the active variables will be reseted: a string will be set to ``""``, 
a number to ``0``, an object to ``{}`` and a boolean to ``false``

To preserve an element from beeing flushed you can pass it to the function: ``flush("item")``

``activate(["item1", "item2"])``: set active the given items

``isActive("item")``: return true or false, usefull for v-show

``isInactive("item")``: return true or false

.. highlight:: django

:: 

   this.activate(["myitem"]);
   

Get and post data
^^^^^^^^^^^^^^^^^

``loadData(url, action)``: loads data and process actions on it

:: 

   function error(err) {
      console.log(err)
   }
   function action(data) {
      console.log(data)
   }

   this.loadData("{% url 'myurl' %}", action, error);
   

``postForm(url, data, action, error, csrfmiddlewaretoken)``: post a form

Note: the ``csrfmiddlewaretoken`` is optional an will be set from the session cookie if not provided

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
      var form = document.getElementById("myform");
      var data = this.serializeForm(form);
      this.postForm(url, data, action, error, data.csrfmiddlewaretoken)
   },

Pass the form token if posting a Django form, otherwise use the session cookie

Shortcuts
^^^^^^^^^
   
``str(json_obj)``: shortcurt for pretty JSON.stringify

``get("id")``: shortcurt for document.getElementById

``query(querystring)``: shortcurt to encode a Graphql query: does '/graphql?query='+encodeURIComponent(querystring)


 