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

1. The positive file: This file is a ```.info``` file which contains the path of all the positive examples, alongside with the number fo objects in that image and a group of squares that indicates where the object are in the image.
2. The negative file: This is a ```.txt``` file which simple contains the path of all the negative images.

Both files can be created with ```create_info_file.py```, if you want to make the negative file you will need to pass ```-ws``` argument. It also only works when the positives examples ARE the object you are looking for. Meaning the ```.info``` file if filled with:

```
PATH_OF_THE_IMAGE 1 0 0 width height
```

Also consider that the OpenCV application WON'T work on Windows if the path has a blankspace on it.

Now you have to use the first OpenCV application ```opencv_createsamples```, I never was able to call it from somewhere else more convenient so I just had to use it from the source folder, in my case it was in: ```~OCV_Folder\build\x86\vc11\bin``` you can change the ```x86``` to ```x64``` if you are working with another architecture.

So you have to put your ```.info``` file and your ```.txt``` file there, open a command windows and type the following:

```
> opencv_createsamples.exe -info YOUR_INFO_FILE -num NB_OF_POS_EXAMPLES -w WIDTH -h HEIGTH -vec OUTPUT_FILE
```

The width and height in the arguments represent the ones from the training window. It's very important to use a training windows similar in dimentions to the image. Again, there's no "good" training window size, you will just have to test many of them. This will output a ```.vec``` file.

Now you will use the next OpenCV application ```opencv_traincascade```. This will output the ```.xml``` that you will use to detect the objects. First setup a folder which will contain all the output files for the training, make sure the file path doesn't contain any whitespaces.

```
> opencv_traincascade.exe -data OUTPUT_FOLDER_PATH -vec VEC_FILE -bg NEG_EXAMPLES_FILE -numPos NUM_POS -numNeg NUM_NEG  -numStages NB_OF_STAGES -w WIDTH -h HEIGHT -featureType FEATURE_TYPE
```

For the algorythm to work, NUM_POS needs to be less than the actual number of positive examples (otherwise it will end prematurely), make sure that the width and height is the same that the ones you ued for the vec file. Again, the number of stages and the feature will come from experience. This will output a lot of file, but the one named ```cascade.xml``` will be the one to use.

## Contact me
