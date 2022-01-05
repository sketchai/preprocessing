from typing import List

import pickle
import argparse
import os
from posixpath import join

import numpy as np
import torch

from sketchgraphs.data import flat_array, sequence, dof

from maps.maps import *
from maps import discretization
from preprocessing_utils import normalization, weighter

from multiprocessing import Process

lMax = 60
lMin = 5
dof_max = None
n_bins = 50




    


def full_preprocess(fi, fo, lMax, lMin, dof_max, n_bins, n_slice):
    try:
        data = flat_array.load_dictionary_flat(f_i)['sequences']
    except:
        data = flat_array.load_flat_array(f_i)
    apply_filters(conf, n_slices)
    sift(fi, fo, lMax, lMin, dof_max, n_slice)
    encode(fo +'_filtered.npy', fo, lMax, n_bins)
    export_parameters(os.path.dirname(fo)+'/', lMax, lMin, dof_max, n_bins)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, help="Input .npy file.")
    parser.add_argument('-o', type=str, help="Output file (without extension).")
    
    parser.add_argument('--lMax', type=int, default=lMax, help="Truncate the sequences.")
    parser.add_argument('--lMin', type=int, default=lMin, help="Truncate the sequences.")
    parser.add_argument('--dof_max', type=int, default=dof_max, help="Set a bound on admissible remaining dof.")
    parser.add_argument('--n_bins', type=int, default=n_bins, help="Discretisation bins.")
    parser.add_argument('--parallel', type=bool, default=False)
    parser.add_argument('--nthreads', type=int, default=5, help="Should divide the number of input files.")
    parser.add_argument('--n_slice', type=int, default=1, help="Number of slices for parallel preprocessing.")
    parser.add_argument('--folder', type=str, default='data/sg_train/', help="Folder containing input files for parallel preprocessing.")

    args = vars(parser.parse_args())
    
    if not(args['parallel']):
        full_preprocess(args['i'], args['o'], args['lMax'], args['lMin'],
                        args['dof_max'], args['n_bins'], args['n_slice'])
        #sift(args['i'], args['o'], args['lMax'], args['lMin'], args['dof_max'])
        #encode(args['o']+'_filtered.npy', args['o'], args['lMax'], args['n_bins'])
        #export_parameters(os.path.dirname(args['o'])+'/', args['lMax'], args['lMin'],
        #                  args['dof_max'], args['n_bins'])
    else:
        nthreads = args['nthreads']
        totalFiles = 0
        for _, _, files in os.walk(args['folder']):
            for _ in files:
                totalFiles += 1
        div, rem = divmod(totalFiles, nthreads)
        assert rem == 0
        assert totalFiles == args['n_slice']
        for i in range(div):
            processes = []
            for j in range(nthreads):
                p = Process(target=full_preprocess, 
                            args=(args['folder']+'slice_'+str(nthreads*i+j)+".npy",
                                  args['folder']+'slice_'+str(nthreads*i+j),
                                  args['lMax'], args['lMin'], args['dof_max'],
                                  args['n_bins'], args['n_slice']))
                p.start()
                processes.append(p)

            for p in processes:
                p.join()


if __name__ == '__main__':
    main()
