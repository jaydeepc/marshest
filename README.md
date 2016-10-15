
[![PyPI version](https://badge.fury.io/py/marshest.svg)](https://badge.fury.io/py/marshest) #maRshEST

maRshEST is mainly a simple marshalling model that can be used to serialize and de-serialize RESTful requests/responses. (JSON only as of now). Also, it provides a wrapper at the top of Python's [requests](http://docs.python-requests.org/en/master/) library, integrated with the MarshMallow base models. 

**maRshEST** is created mainly for performing automated testing of REST APIs.

## Installation

To install MarshMallow just use pip:

`pip install marshest`

maRshEST requires Python 3.X or more. However, this should work with python 2.7.x as well, but its not tested.

##Documentation

To serialize and de-serialize your HTTP request and response, you need to implement the `_object_to_json` and `_json_to_object` methods which are provided by MarshModel class. For interacting with your REST APIs, you need to have different Business specific methods, which will use your models, so that it can be easily accessed by your tests, in the form of objects. 

Lets see how to implement the above jargons to make your API functional tests simple and readable.

For example purpose, lets use one of the dummy APIs provided by [ReqRes](http://reqres.in/api/users?page=2).

We will use the below API which makes a **POST** call to create users. Details of the API are:

**Request URL**: `http://reqres.in/api/users`

**Request Method**: `POST`

**Request Payload**: `{
    "name": "morpheus",
    "job": "leader"
}`

On successful request, the response details are:

**Response Code**: `201`

**Response Body**: 

	{
	    "name": "morpheus",
	    "job": "leader",
	    "id": "387",
	    "createdAt": "2016-10-14T20:33:59.437Z"
	}


How to write a functional test using MarshMallow is provided in [this example](https://github.com/jaydeepc/marshmallow_example). 

PS: I have used pytest to run the tests, but you can use any runner you want. The concept is same. 

In the example, you will see that apart from the test file, I have a `user_models.py` and a `user_apis.py`. In `user_models.py`, we have two classes. One for serializing the CREATE (or POST) request payload and one for De-serializing the Response, both extending parent MarshModel. As mentioned earlier, the serializer method that is implemented in your client and defined on MarshModel, is `_object_to_json`. And for deserializing the same is called, `_json_to_object`. 

The `user_apis.py` basically provides methods each representing one business API. They take necessary params to make the call and returns the deserialized object, which can be used to assert various cases. This also extends from the MarshClient which is a wrapper around python's `request` library, integrated with MarshModels.

Below diagram should give a more clear idea of what's going on:

![MarshMallow](https://github.com/jaydeepc/marshmallow_example/blob/master/maRshEST.png)

So, what happens here is, the Tests only understands the language of Object and hence with that language, makes a call to the client. The Client then uses the model where the `_object_to_json` is implemented to get the payload in JSON form and then makes a Request to the API, which understands only JSON language (or XML). The API the returns the JSON response back to Client and client asks model to user `_json_to_object` to convert it to object and gives it back to the test.




