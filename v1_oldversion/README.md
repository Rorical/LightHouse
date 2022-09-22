# Lighthouse-Blind Guidance System

#### Project Members: Codie Liu, Tristan Yang
#### Project Instructors: Samuel Jia, Johnson Zhang
#### Author of Log: Tristan Yang


## Introduction:
The project that we are working on is a guidance system for blind people, with a combination of a helmet and a cane with built in sensors.

## Plan analysis:

1.	Our first plan was a series of built-in radars surrounding the edge of the helmet using TOF (Time of Flight).
TOF has a number of advantages, it can possess 300 thousand effective depth information points, 10 times than that possessed by structured light. As a result, it is very accurate at identifying objects, gestures, etc. It especially professes at indoor navigation, a very important and often challenge task for the blind community.

2.	Our second plan was to help blind people navigate using artificial sound effects. According to our interviews with the blind community, indoor navigation can be handled with touch and a cane. Navigating outdoors is more complex though. In the words of a 40-year-old blind man, “I have to walk very slowly and carefully on the street, otherwise I run the risk of hitting a street lamp, it is very frustrating, I wish I had the ability to walk more freely.” 
With this information, we fixed our attention to an obvious fact, blind people rely on hearing, which means that their acoustic sense is better than most people. This made us come up with an idea. What if we can artificially make obstacles emit sound, by creating a virtual acoustic space so that blind people can tell the location of the obstacles through these artificially made sound. This can be used to locate both moving and static objects, making it very useful in street navigation.

## Execution:

1.	Our plan is to use a spinning TOF radar in front of a helmet, and transmitting the location signals to the blind person via a series of vibration motors in front of the hat.

