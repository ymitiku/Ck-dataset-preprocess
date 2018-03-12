import cv2
import dlib 
import os
from sklearn.model_selection import train_test_split
import numpy as np
EMOTIONS = {
    0:"neutral", 1:"anger", 2:"contempt", 3:"disgust", 4:"fear", 5:"happy", 6:"sad", 7:"surprise"
}



def get_all_sequence_paths(dataset_path):
    """ gets path to all sequences inside dataset_path folder
    Parameters
    ----------
    dataset_path : str
        Path to the dataset folder.
    Returns
    -------
    output : list
        List of path to sequences inside dataset_path. The path is folder
        heirarchy from dataset_path folder to sequnece folder
    """
    output = []
    if os.path.isdir(dataset_path):
        for subj_dir in os.listdir(dataset_path):
            if  os.path.isdir(os.path.join(dataset_path,subj_dir)):
                for sequnce_dir in os.listdir(os.path.join(dataset_path,subj_dir)):
                    output.append([dataset_path,subj_dir,sequnce_dir])
    return output

def remove_non_image_files(image_names,image_ext):
    output = []
    for img_name in image_names:
        _,ext = os.path.splitext(img_name)
        if ext in image_ext:
            output+=[img_name]
    return output

def split_ck_dataset_helper(sequences_path,emotion_path,output_path,detector,max_emotion_images):
    
    if not os.path.exists(os.path.join(output_path, "neutral")):
        os.mkdir(os.path.join(output_path, "neutral"))

    if not os.path.exists(output_path):
        os.mkdir(output_path)
    if not os.path.exists(os.path.join(output_path, "neutral")):
        os.mkdir(os.path.join(output_path, "neutral"))

    for seq_path in sequences_path:
        if os.path.isdir(os.path.join(*seq_path)):
            sequence_images_names = os.listdir(os.path.join(*seq_path))
            sequence_images_names = remove_non_image_files(sequence_images_names,[".png",".PNG"])
            sequence_images_names.sort()
            if not os.path.exists(os.path.join(emotion_path,seq_path[1],seq_path[2])):
                print "No emotion label inside ",os.path.join(emotion_path,seq_path[1],seq_path[2])
                continue
            emotion_files = os.listdir(os.path.join(emotion_path,seq_path[1],seq_path[2]))
            if len(emotion_files)==0:
                print "No emotion label inside ",os.path.join(emotion_path,seq_path[1],seq_path[2])
                continue
            emotion_file = emotion_files[0]
            emotion = np.loadtxt(os.path.join(emotion_path,seq_path[1],seq_path[2],emotion_file))
            emotion = int(emotion)
            if emotion == 2:
                continue
            emotion_string = EMOTIONS[emotion]
            neutral_image = cv2.imread(os.path.join(seq_path[0],seq_path[1],seq_path[2],sequence_images_names[0]))
            if neutral_image is None:
                print "Unable to read image from ", os.path.join(os.path.join(seq_path[0],seq_path[1],seq_path[2],sequence_images_names[0]))

            neutral_face = detector(neutral_image)[0]
            neutral_face_image = neutral_image[
                max(0,neutral_face.top()):min(neutral_face.bottom(),neutral_image.shape[0]),
                max(0,neutral_face.left()):min(neutral_face.right(),neutral_image.shape[1])
            ]
            cv2.imwrite(os.path.join(output_path,"neutral",sequence_images_names[0]),neutral_face_image)
 
            if not os.path.exists(os.path.join(output_path,emotion_string)):
                os.mkdir(os.path.join(output_path,emotion_string))

            for i in range(len(sequence_images_names)-1,len(sequence_images_names)-1-max_emotion_images,-1):
                image = cv2.imread(os.path.join(seq_path[0],seq_path[1],seq_path[2],sequence_images_names[i]))
                faces = detector(image)  
                if len(faces)==0:
                    print "No faces found for: ",os.path.join(seq_path[0],seq_path[1],seq_path[2],sequence_images_names[i]), " image"
                    continue
                face_image = image[
                    max(0,faces[0].top()):min(faces[0].bottom(),image.shape[0]),
                    max(0,faces[0].left()):min(faces[0].right(),image.shape[1])
                ]
                cv2.imwrite(os.path.join(output_path,emotion_string,sequence_images_names[i]),face_image)
                





def split_ck_dataset(dataset_path,emotion_path,output_path,max_emotion_images,test_size=0.2):
    """ Splits ck dataset into train and test datasets. The method makes the 
    following assumtions.
        1. The images sequence path is dataset_path
        2. The subject folders are inside dataset_path folder
        3. The image sequences folders are inside subject folder which is inside dataset_path folder
        4. The names of images inside sequence folders have sequential number appened to common name 
            all image inside that folder and this sequetial number is crosspond to frame number of
            the sequence. 
        5. The respective emotion label for each sequence folder is inside emotion_path
        6. Parent directory of output_path exists
        7. max_emotion_images is less length each sequence
    Using this assumtions the method first get splits the sequences into train and test sequences. Then 
    reads all sequence images. The method labels the first image in sequence as neutral and the last n
    (where n is max_emotion_images arg) images as label specified in Emotion folder for respective sequence. 
    Parameters
    ----------
    dataset_path : str
        Path to ck+ image sequences(raw images downloaded from official website of ck+ dataset)
    emotion_path : str
        Path to Emotion folder downloaded from official website of ck+ dataset
    output_path : str
        Output folder to save images
    max_emotion_images

    """

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    detector = dlib.get_frontal_face_detector()
    sequences_path = get_all_sequence_paths(dataset_path)
    
    train_sequences_paths,test_sequences_paths = train_test_split(sequences_path,test_size=test_size)

    if not os.path.exists(os.path.join(output_path,"train")):
        os.mkdir(os.path.join(output_path,"train"))
    if not os.path.exists(os.path.join(output_path,"test")):
        os.mkdir(os.path.join(output_path,"test"))

    

    split_ck_dataset_helper(train_sequences_paths,emotion_path,os.path.join(output_path,"train"),detector,max_emotion_images)
    split_ck_dataset_helper(test_sequences_paths,emotion_path,os.path.join(output_path,"test"),detector,max_emotion_images)