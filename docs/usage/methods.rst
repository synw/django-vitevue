Available methods
=================

State management
^^^^^^^^^^^^^^^^

A basic state management mechanism is used to manage the display. Methods:

``flush()``: reset all active items

To preserve an element from beeing flushed you can pass it to the function: ``flush("item")``

``activate(["item1", "item2"])``: set active the given items

``isActive("item")``: return true or false, usefull for v-show

.. highlight:: django

:: 

   this.flush();
   this.activate(["myitem"]);
   

Get and post data
^^^^^^^^^^^^^^^^^

``loadData(url, action)``: loads data and process actions on it

:: 

   function action(data) {
      console.log(data)
   }

   this.loadData("{% url 'myurl' %}", action);
   

``postForm(url, data, action, error, csrfmiddlewaretoken)``: post a form

Note: the ``csrfmiddlewaretoken`` is optional an will be set from the session cookie if not provided

::

   function error(err) {
    console.log(err)
   }
   function action(response) {
    console.log(response)
   }
   # formdata is a json object
   this.postForm(url, formdata, action, error, myform.csrfmiddlewaretoken)

Pass the form token
if posting a Django form, otherwise use the session cookie
   
``str(json_obj)``: shortcurt for pretty JSON.stringify


 