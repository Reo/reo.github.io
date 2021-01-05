---
layout: post
author: Leo
section: blog
title: "API Authorization Technologies"
category: programming
tags: web API authentication
mathjax: false
---

This week, I go over the technologies involved in an implementation of the API authorization project
mentioned previously. This includes a discussion on how communication takes place on the internet
and preliminaries on authentication.

Recall we wish to make an application which, when prompted, will fetch new course content
(eg. assignments) not already downloaded. For each item which is added, a task will be created in
a todo list using the WunderList API.

Let's begin with the actual fetching of the content from a given site. In other words, let's be more
precise about what it means to download a1.pdf from `http://www.school.math.ca/course/assignments/`.
What is commonly referred to as a URL (Uniform Resource Locator), is simply a string of characters
which uniquely identifies a resource. In this case, the resource is a file over the network, this
file is often interpreted and handled accordingly by a browser (ie. an HTML file may be formatted
appropriately and shown to the user as a web page while a format which the browser does not support
would often be downloaded for the user to choose how to open it). Also note that a URL is simply
a specific type of URI (Uniform Resource Identifier). The URI generic syntax has five components of
which only two are required:

`scheme:[//authority]path[?query][#fragment]`

Further, the authority section consists of:

`[UserInfo@]host[:port]`

- The **scheme** tells the browser how to interpret everything which follows the colon.
- **Authority** is optional and though the UserInfo section will not be relevant for our discussion, we
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
access to locally stored files and _http_ which will be of particular interest for this project.
http is a protocol which allows requests to be sent for the server to respond accordingly. These
requests is how the server knows what to do with the data at the specified URI and include `GET`,
`POST`, and `PATCH`. A file (eg. HTML file or "web page") being fetched by a browser, is an example
of a `GET` request. The server can then send a code which represents the status of what has
occurred. Some common codes include `404` and `200` which mean a resource was not found and
a response went through well (or "OK") respectively.

Communicating with a server using only codes would obviously be incredibly restrictive so the `GET` and
`POST` are frequently used to send data back and forth between the client and server in
a standardized format. There a number of these standardized formats, the one relevant to this
project being the JSON format which WunderList API uses to respond to requests. JSON objects consist
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
relevant to our project since the WunderList API uses authentication to ensure users are not able to
perform actions they would not be able to normally. For authentication, the WunderList API uses the
"authorization code" flow for oAuth 2 where we obtain the access token then simply paste the acquired
access token in the application which uses a CLI.

More specifics with regards to the authorization process will be presented in the next post
where we go over an implementation using the flow described in the documentation for usage of
WunderList's API and oAuth2.
