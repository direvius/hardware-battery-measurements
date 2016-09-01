import pandas as pd
import seaborn as sns
import numpy as np
import collections
import matplotlib.pyplot as plt
import logging
import argparse
#%matplotlib inline

def input_files_to_df(files, suffix, delimiter):
    work_df = None

    for work_file in files:
        filename = work_file.split('/')[-1]
        if work_df is None:
            work_df = pd.read_csv(work_file, delimiter=delimiter, names="ts curr".split())
            work_df['label'] = '{name}_{suffix}'.format(name=filename, suffix=suffix)
        else:
            df = pd.read_csv(work_file, delimiter=delimiter, names="ts curr".split())
            df['label'] = '{name}_{suffix}'.format(name=filename, suffix=suffix)
            work_df = work_df.append(df)

    #convert unixtimestamp to datetime/s
    work_df['ts'] = pd.to_datetime(work_df['ts'],unit='s')

    #drop NaN and drop label column
    for key, df in work_df.groupby('label'):
        df.drop('label', axis=1, inplace=True)
        df.dropna()

    return work_df

def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('--suffix', type=str, help='Common suffix for output', default='')
    parser.add_argument('--delimiter', type=str, help='Common delimiter for CSV', default=' ')
    parser.add_argument('files', type=str, nargs='+', help='Input files')
    parser.add_argument('--to-dir', default='.')
    args = parser.parse_args()

    try:
        logging.debug("Started output generation")
        logging.info("Input files: %s", args.files)

        df = input_files_to_df(args.files, args.suffix, args.delimiter)

        #barplot
        logging.info("Started rendering plot")
        sns.set(font_scale=1, rc={"figure.figsize": (10, 5)})
        ax = sns.barplot(x=df.label, y=df.curr)

        for p in ax.patches:
            height = p.get_height()
            ax.text(p.get_x(), height+2, '%1.2f' % (height) )

        plt.ylabel('mean(current), mA')
        plt.savefig(args.to_dir+'/barplot.png')
    except Exception as exc:
        logging.error("Failed output generation: %s", exc)
    else:
        logging.info("Successfully finished")

if __name__ == '__main__':
    main()
