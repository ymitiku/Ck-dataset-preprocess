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

    parser.add_argument("-d","--dataset_path",default=None,type=str)
    parser.add_argument("-e","--emotion_path",default=None,type=str)
    parser.add_argument("-m","--max_emotion_images",default=3,type=int)
    parser.add_argument("-t","--test_size",default=0.2,type=float)
    parser.add_argument("-o","--output_path",default=None,type=str)
    parser.add_argument("-s","--sequence",default=False,type=bool)
    parser.add_argument()

    args = parser.parse_args()
    return args


def main():
    args = get_cmd_args()
    split_ck_dataset(args.dataset_path,args.emotion_path,args.output_path,args.max_emotion_images,test_size=0.2,sequence=args.sequence)
    

if __name__=="__main__":
    main()