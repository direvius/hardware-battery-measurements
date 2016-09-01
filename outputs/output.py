import pandas as pd
import seaborn as sns
import numpy as np
import collections
import matplotlib.pyplot as plt
import logging
import argparse
#%matplotlib inline

def input_files_to_df(files, suffix, delimiter):
    work_dict = {}

    #read csv to df
    for work_file in files:
        filename = work_file.split('/')[-1]
        work_dict[filename] = pd.read_csv(work_file, delimiter=delimiter, names="ts curr".split())
        work_dict[filename]['ts'] = pd.to_datetime(work_dict[filename]['ts'],unit='s')

    #make sorted dict of dataframes
    work_dict_sorted = collections.OrderedDict(sorted(work_dict.iteritems()))
    solid_df = None
    #add label to each dataframe
    for key, df in work_dict_sorted.iteritems():
        df['label'] = "{key}_{suff}".format(
            key=key,
            suff=suffix
        )

        #drop NaN
        df.dropna()

        #consolidate dict -> dataframe
        if solid_df is None:
            solid_df = df
        else:
            solid_df = solid_df.append(df)
    return solid_df

def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('--suffix', type=str, help='Common suffix for output', default='')
    parser.add_argument('--delimiter', type=str, help='Common delimiter for CSV', default=' ')
    parser.add_argument('files', type=str, nargs='+', help='Input files')
    parser.add_argument('--to-dir', default='.')
    args = parser.parse_args()

    try:
        logging.debug("Start output generation")
        logging.info("Input files: %s", args.files)

        df = input_files_to_df(args.files, args.suffix, args.delimiter)
        #barplot
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
