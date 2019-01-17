---
layout: post
title: "API Authorization Technologies"
date: 2019-01-16
category: programming
tags: project web technology
author: "Reo"
---

This week, I go over the techonologies involved in an implementation of the project mentioned in the
last post. Recall we wish to make an application which, when prompted, will fetch new course content
(eg. assignments) not already downloaded. For each item which is added, a task will be created in
a todo list using the Wunderlist API.

Let's begin with the actual fetching of the content from a given site. In other words, let's be more
precise about what it means to "download a1.pdf from http://www.school.math.ca/course/assignments/".
What is commonly reffered to as a URL (Uniform Resource Locator), is simply a string of characters
which uniquely identifies a resource. In this case, the resource is a file over the network, this
file is often interpreted and handled accordingly by a browser (ie. an HTML file may be formatted
appropriatelly and shown to the user as a webpage while a format which the browser does not support
would often be downloaded for the user to choose how to open it). Also note that a URL is simply
a specific type of URI (Uniform Resource Identifier). The URI generic syntax has five components of
which only two are required:

`scheme:[//authority]path[?query][#fragment]`

Further, the authority section consists of:

`[userinfo@]host[:port]`


- The **scheme** tells the browser how to interpret everything which follows the colon.
- **Authority** is optional and though the userinfo section will not be relevant for our discussion, we 
  will be using the host and port sections which follow it.
	- **host** consists either of a registered name or an ip address
	- **port** is an endpoint used for communication associated with an IP address and
	  a protocol. These are identified by a 16-bit unsigned integer.
- The **path** is a slash-separated sequence of segments which often is the directory to the desired
  resource.
- The **query** often consists of key-value pairs separated by a delimiter. This delimiter
  usually takes the form of ";" or "&" characters.
- For our purposes, **fragment** will consist of more delimiter-separated key-value pairs


The **scheme** deserves special emphasis for this project. Possibilities include _file_ which provides
access to locally stored files and http which will be of particular interest for this this project.
http is a protocol which allows requests to be sent for the serve to respond accordingly. These
requests is how the server knows what to do with the data at the specified URI and include `GET`,
`POST`, and `PATCH`. A file (eg. html file or "webpage") being fetched by a browser, is an example
of a `GET` request. The server can then send a code which represents the status of what has
occurred. Some common codes include `404` and `200` which mean a resource was not found and
a response went through well (or "OK") respectively.

Communicating with a server using only codes would obviously be incredibly restrictive so the `GET` and
`POST` are frequently used to send data back and forth between the client and server in
a standardized format. There a number of these standardized formats, the one relevant to this
project being the JSON format which Wunderlist API uses to respond to requests. JSON objects consist
of key-value pairs like such:

```javascript
myObj = {
name:    "John Smith"
tel:     "+1-123-123-1234"
address: "38 example dr."
}
```

As one can imagine, more care must be taken when the requests involve more delicate data such as
user information. These sorts requests are usually dealt with using some sort of authentication so
the information is only released by the server if the authentication has been done properly. This is
relevant to our project since the Wunderlist API uses authentication to ensure users are not able to
perform actions they would not be able to normally. For authentication, the Wunderlist API uses the
"authorization code" flow for oAuth 2, in order to not overwhelm the amount of concepts introduced
here we will first have to create a web app to obtain the access token then simply paste the aquired
access token in the application which uses a CLI.

More specifics with regards to the authorization process will be presented in the next post
where we go over an implementation using the flow described in the documentation for usage of
Wunderlist's API and oAuth2.

