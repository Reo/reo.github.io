---
layout: post
author: Leo
section: blog
category: etc
title: API-Authorization-Primer
---

Here we create
create a simple application to keep track of assignments in a todo list. We
interface with the Wunderlist API to achieve this. This post goes over a motivation and some
some specifications while future posts will cover more in detail.

I like to keep track of tasks I should complete along with some ordering where the priority is often
dictated by the due date and an estimate of how long it would take to complete. School assignments
in particular are a form these tasks may take and are particularly nice in that the due dates are
well defined and the work involved is often consistent within a course. This makes them a good
candidate for automation and that is exactly what this project is about.

As the blurb at the top alludes to, I use Wunderlist to keep track of what I have to get done and by
when so we will be using the Wunderlist API. As for the language of choice, the point of this project
is more so to learn to interact with web APIs at a high level and create something which can be
invoked to run the job for us. In my experience, Python will make this convenient.
