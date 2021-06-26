---
layout: post
author: reo
title: 'Using the ATT&CK Framework to Study Ryuk Ransomware'
category: malware
tags: MITRE 'ATT&CK'
---

It has become common to see the disasterous effects of ransomware
making front-page news. Everywhere from
[hospitals](https://globalnews.ca/news/7963652/humber-river-hospital-ransomware-attack-toronto/)
to
[meat suppliers](https://arstechnica.com/gadgets/2021/06/attack-on-meat-supplier-came-from-revil-ransomwares-most-cut-throat-gang/),
it seems to paint a tragic picture with little hope.
This is why a Red Canary article describing
[how a hospital staved off a Ryuk ransomware outbreak](https://redcanary.com/blog/how-one-hospital-thwarted-a-ryuk-ransomware-outbreak/)
caught my attention. The article uses the ATT&CK
attack framework to describe the behaviour of the malware
and points where it may be detected before causing potentially
irrepairable damage.

## Contents
{:.no_toc}

* Content
{:toc}

<br>

* * *

## ATT&CK and Threat Intelligence

* * *

Adversarial Tactics, Techniques, and Common Knowledge (ATT&CK)
is a framework which classifies offensive behaviours which
have been observed in real breaches across many different industries.
As Katie mentions in the
[getting started](https://medium.com/mitre-attack/getting-started-with-attack-cti-4eb205be4b2f)
blog post,

> Cyber threat intelligence is all about knowing what your adversaries
> do and using that information to improve decision-making.

In the aforementioned Red Canary article, the team also
highlights the importance of looking at the tactics, techniques,
and procedures (TTP) used by the adversary. In fact, the Red Canary
team also attributes intelligence from external sources for reporting
on previous beraches involving Ryuk and related malware
(see
[this post](https://thedfirreport.com/2020/10/18/ryuk-in-5-hours/)
on The DFIR Report for instance).

MITRE lays out the tactics and techniques in a matrix which makes visualization
easier than most documents and leads us to our next point.

<br>

* * *

## The ATT&CK Navigator

* * *

One of the reasons I find the matrix layout to be particularly convenient from the point of
view of someone studying an attack, is that it allows for the creation of a so-called
**Navigation Layer**. This navigation layer creates what looks like a trace of the attack
making it a great visualization tool allowing one to more easily identify patterns; making
spotting the same strain of malware, or possibly a new one which behaves similarly, easier.

The Red Canary article also includes an incident Navigation Layer which is public and can
be seen [here](https://github.com/redcanaryco/public-research/blob/master/intelligence/20201029-Bazar-Cobalt-Strike-Incident-Navigator-Layer.json).
It's possible to then view the colour-coated ATT&CK matrix with commentary using
the
[ATT&CK Navigator](https://github.com/mitre-attack/attack-navigator).

|![Att&ck Navigator Example](/assets/images/attack-navigator.png){: style="text-indent: 0;" class="invert-color"}|
|:--:|
| *Hovering over a Technique in the Attack Navigator* |

Including comments here allows teams to include details of the observed behaviour
highlighting techniques which may be indicative of an ongoing attack as well as possible
preventive measures as seen in the above image.

<br>

* * *

## Conclusions

* * *

I think the conclusion in
[Finding Cyber Threats with ATT&CK-Based Analytics](https://www.mitre.org/publications/technical-papers/finding-cyber-threats-with-attck-based-analytics)
phrases it well. Advanced Persistent Threats (APTs) aren't going anywhere
anytime soon so having a tool
to base analytics on which is capable of detecting these threats will
only continue to increase in value.

Of course, this is only scraping the surface and most of this would be automated
with the help of repositories such as MITRE's [CAR](https://car.mitre.org/) and
reinforced with organization-specific metrics and baselines.
There is additionally
Disaster Recovery and Business Continuity plans to take into account since, as with anything
in cyber security, there is no silver bullet.

<br>

* * *

## References

* * *

Main Red Canary article being referenced

- `https://redcanary.com/blog/how-one-hospital-thwarted-a-ryuk-ransomware-outbreak/`

Ransomware Breaches

- `https://globalnews.ca/news/7963652/humber-river-hospital-ransomware-attack-toronto/`
- `https://arstechnica.com/gadgets/2021/06/attack-on-meat-supplier-came-from-revil-ransomwares-most-cut-throat-gang/`

misc

- `https://medium.com/mitre-attack/getting-started-with-attack-cti-4eb205be4b2f`
- `https://thedfirreport.com/2020/10/18/ryuk-in-5-hours/`
- `https://www.mitre.org/publications/technical-papers/finding-cyber-threats-with-attck-based-analytics`

