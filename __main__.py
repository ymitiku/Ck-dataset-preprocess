from __init__ import split_ck_dataset

import argparse


def get_cmd_args():
    """Gets cmd arguments.
    Returns
    -------
    args : dict
        Dictionary containg cmd arguments.        
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--dataset_path",default=None,type=str)
    parser.add_argument("--emotion_path",default=None,type=str)
    parser.add_argument("--output_path",default="models/model.h5",type=str)
    parser.add_argument("--max_emotion_images",default=3,type=int)
    parser.add_argument("--test_size",default=0.2,type=float)

    args = parser.parse_args()
    return args


def main():
    args = get_cmd_args()
    split_ck_dataset(args.dataset_path,args.emotion_path,args.output_path,args.max_emotion_images,test_size=0.2)
    

if __name__=="__main__":
    main()