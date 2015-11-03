# CartoonRecognizer

1. Introduction
2. Software Requirements
3. How to use
  1. How to train your own detector
4. Contact me

## Introduction

## Software Requierements

## How to use
### How to train your own detector
In this section I will show how to train an object cascade detector using OpenCV applications.

First of all you will need A LOT of images of the object you are looking for, the more the merrier. For a solid and unchanging object like a logo few will suffice, but if you are looking for faces, you'll need hundreds or even thousands examples.

Apart from that you will need images of negative examples that will be used as background for the training. The negative images can be anything and everything that does NOT contain the object you are looking for.

There is really no "good" number of images for the positive or the negative. You'll just have to get to the number by experience.

Once you have all the images you want you will need two files:

1. The positive file: This file is a ```.info``` file which contains the path of all the positive examples along with a "1" and a square that indicates where the object is in the image.
2. The negative file: This is a ```.txt``` file which simple contains the path of all the negative images.

Both files can be created with ```create_info_file.py```, if you want to make the negative file you will need to pass ```-ws``` argument. It also only works when the positives examples ARE the object you are looking for. Meaning the ```.info``` file if filled with:

```
PATH_OF_THE_IMAGE 1 0 0 width height
```

Also consider that the OpenCV application WON'T work on Windows if the path has a blankspace on it.

## Contact me
