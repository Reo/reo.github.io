---
layout: post
title: "API-Authorization-Implementation"
date: 2019-01-23
category: programming
tags: python project web code requests
author: "Reo"
---

This post covers an implementation of the project we have been discussing for the last two posts.
Recall that the goal was to create a simple program which would fetch assignments from a set of
courses and add them as tasks to be done in a Wunderlist todo list using the API.

For this project, we will be using the Python requests library which strikes a nice balance between
concise and descriptive code for our purposes. Last time we went over details
regarding URL and http requests both of which will apply heavily this post, though this post also
includes the added aspect of authentication using oAuth2.

Seeing as the focus is the requests I will very briefly go over the part of the script which does not
deal with the topic at hand.

```python
import requests
from requests_oauthlib import OAuth2Session
import random
import string

courseCode = raw_input("enter the course code to be fetched: ")
assign_num = raw_input("enter assignment number to be fetched: ")
padded_assign_num = assign_num if (int(assign_num) > 9) else "0"+assign_num

course_site = {'MAT101': 'https://www.math.school.ca/course/Prob_Set_'+ padded_assign_num + '.pdf'}

# error checking
if (not courseCode in course_site.keys()):
    print("please enter a defined course or add one, defined courses:")
    for course in course_site:
        print(course)
    quit()
```

`course_code` and `assign_num` are simply values from the user which are used to download the
correct assignment and used as the title of the task (eg. a task may be "MAT101 assignment 1").
`padded_assign_num` is used for assignment URLs which pad single digit numbers with a 0.
`course_site` simply maps course codes to the respective URL to fetch the assignments. And finally,
the if statement is error checking to make sure that the course code is in fact a key in the
dictionary.

Now, a simple request to `GET` a file may be written as follows using the requests library:

```python
# URL to which get request will be sent
assign_url = course_site[course_code]

# perform the GET request to assign_URL
assign_request = requests.get(assign_url, allow_redirects=True)

# status code error checking
if (assign_request.status_code == 200):
    open('q'+assign_num+".pdf", 'wb').write(assign_request.content)
    print("successfully downloaded!")
else:
    print("assignment %s does not exist" % assign_num)
    quit()
```

Note the scheme specified in the URI, http(s), defines the `GET` operation
[as we have gone over][API tech].
`assign_request` is an object which now holds the response from the server. We
remember from the last post that
a status code of `200` indicates "OK" so that is the response we are looking for from this request,
anything else indicates something went wrong (presumably `404`, the assignment is not up yet). With
the assignment downloaded, we now wish to get into the meat of the
project, interacting with the WunderList API.

The flow which WunderList specifies in its documentation is the "authorization code" flow,
typically reserved for web apps on a server (for reasons we will go into in a bit). We will be
following [WunderList's developer
documentation](https://developer.wunderlist.com/documentation/concepts/authorization).

The steps for using "authorization code" flow would be as follows:

1. The user makes a request to log in
2. The application redirects the user to the Authorization server (`/authorize` endpoint)
    - note, the params required here may change depending on the API in question, in our case,
        WunderList requests we send our **client id**, **redirect uri**, and an "unguessable"
        **state** as parameters
3. The aforementioned authorization server redirects the user to the login prompt
4. The user authenticates using one of the configured login options
5. WunderList's authorization server redirects to a **redirect uri** with an authorization **code**
6. The cryptographically random **state** generated locally is checked against the one the server sends
   back
7. The **code**, **client id**, and **client secret** are sent to the `/access_token` endpoint
8. The authentication server responds with an **access token**
9. The application uses said **access token** to make requests "as" the user
10. The API responds with the requested information

We begin with the **client id**, **client secret**, **redirect uri**, and **state** which are
mentioned in the steps above. The first three are given upon [completing an
application](https://developer.wunderlist.com/apps/new "create new app"). **redirect uri** is
chosen as a server which runs locally on the machine on an unused port and **state** is "_An
unguessable random string_" which is used to protect against cross-site request forgery attacks.
It would be a good idea to write a function to generate such strings.

```python
def generateRandomString(string_length):
    """Return a randomly generated alphanumeric string of string_length length

    :string_length: length of the string to be created
    :returns:       randomly generated alphanumeric string of string_length length

    """
    # This is simply a string composed of uppercase and lowercase letters as well as digits 0-9.
    alpha_numer=string.ascii_letters + string.digits

    # concatenate string_length alphanumeric characters
    ret=''.join(random.SystemRandom().choice(alpha_numer) for _ in range(string_length))
    return ret


# credentials
client_id = 'client id from application'
client_secret = 'client secret from application'
redirect_uri = 'http://localhost:8888/callback'
local_state = generateRandomString(16)
```

We may now begin with the steps highlighted above.

## Step 1

This is done implicitly in our case. For our purposes, the user opening up WunderFetch would imply
they want to use the capabilities of the WunderList API (and hence log in).

## Step 2

Here, we redirect the user to WunderList's authorization server,
`https://www.wunderlist.com/oauth/authorize`. Like was mentioned in the previous post, information
may be sent as parameters in the query of a URL and as the steps above indicate, we send the **client
id**, **redirect uri**, and **state**. The resulting URL to which the redirect takes place then
looks like:

`https://www.wunderlist.com/oauth/authorize?client_id=<client_id>&redirect_uri=<redirect_uri>&state=<state>`

where `<>` indicates reference to the variables. The requests library does this in a pair of lines:

```python
# oAuth2 session, the params are set here
oauth = OAuth2Session(client_id=client_id, redirect_uri=redirect_uri, state=local_state)

# requests takes responsibility for construction of the query string.
# authorization_url: the newly created URL
# state            : the state which was sent off to the server
authorization_url, state = oauth.authorization_url('https://www.wunderlist.com/oauth/authorize')

print('Please authorize access at: %s' % authorization_url)
```

## Steps 3-5

The user pastes **authorization\_url** in a browser which redirects to the login prompt. The user
authenticates at the redirected URL and gets sent back to
"**redirect\_uri**?state=*state-from-server*&code=*code-from-server*"

## Step 6

The user pastes the values in the param of the final URL, the state sent from the server is then
checked against the locally stored **state** to ensure the authenticity of the request.

```python
state = raw_input('Enter the state param from the callback URL')

if ( state != local_state ):
    print("authorization error, state mismatch.")
    quit()
```

## Step 7

We first receive the **code** from the user (the second parameter in the URL they were redirected
to) and then send this along with the **client id** and **client secret** to
`https://www.wunderlist.com/oauth/access\_token`. The [WunderList
documentation](https://developer.wunderlist.com/documentation/concepts/authorization) specifies we
send this as a `POST` request with the data sent in JSON format. The server then responds with
a JSON object which contains the **access token** required to access the user's data:

```python
code = raw_input('Enter the code param from the callback URL:')

tok_data = {'client_id': client_id, 'client_secret': client_secret, 'code': code}
token = requests.post('https://www.wunderlist.com/oauth/access_token', data=tok_data)
```

## Step 8

We store the access token which the server sent, the requests library may be used to parse the JSON
response as a Python dictionary the key may then be used to grab the access token:

```python
# retrieve access token from JSON format
access_token = token.json()['access_token']
```

## Step 9

All that remains now is to make the requests using the newly acquired access token --- WunderList's
API requires requests which involve user information are sent with a header with the following
syntax:

`headers = {'X-Access-Token': access_token, 'X-Client-ID': client_id}`

In this case, we wish to add a new task. Referring again to
[the documentation](https://developer.wunderlist.com/documentation/endpoints/task), we do a `POST`
request with the required data. A response of `201` from the server then indicates everything went
as desired:

```python
# WunderList requires this for requests which require authentication
headers = {'X-Access-Token': access_token, 'X-Client-ID': client_id}

# create a task
list_id = 367927829
post_data = {"list_id": list_id, "title": course_code + " assignment " + assign_num}
post_req = requests.post('https://a.wunderlist.com/api/v1/tasks', headers=headers, json=post_data)

if (post_req.status_code == 201):
    print("successfully added task!")
else:
    print("problem creating task, code:" + post_req.status_code)
```

An important note here is that since the course websites and the location of assignments within them
can be vastly different or even randomly generated (for instance, some require padding while others don't in
this example) this demonstration has them hard-coded. There are
numerous ways to improve our situation here, for instance, we can have the script look in a locally
stored file which contains the key-value pairs of the courses and their respective websites.

Thank you for reading, the full source code can be found on the [GitHub repository](https://github.com/Reo/FetchAndTodo).

[API tech]: /programming/2019/01/16/API-Authorization-Technologies.html "API authorization technologies"
