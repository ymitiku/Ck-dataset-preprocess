# Ck+  dataset preprocess

Python module to preprocess ck+ dataset. 

Some basic assumtions.
* The dataset path is given using command line 
* emotion label path is given using command line 
* The subject folders are inside dataset path folder
* The image sequences folders are inside subject folder
* The names of images inside sequence folders have sequential number appened to common name all image inside that folder and this sequetial number is crosspond to frame number of the sequence. 
* The respective emotion label for each sequence folder is inside emotion label folder
* Parent directory of output_path exists
* Max_emotion_images is less than length each sequence
    
Using this assumtions the module first  splits the sequences into train and test sequences. Then reads all sequence images. 
The module labels the first image in sequence as neutral and the last n (where n is max_emotion_images arg) images as label specified in Emotion folder for respective sequence.

## How to run the module 
```
python . --dataset_path path-to-dataset --emotion_path path-to-emotion-labels-folder --output_path path-to-output-directory --max_emotion_images 4 --test_size 0.2
```
