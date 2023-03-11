#!/usr/bin/env python3.7
import pathlib
import pickle

for pkl_file in sorted(pathlib.Path(".").glob("*_dist.pkl")):
	print(f"Read data from {pkl_file}")
	with open(pkl_file, 'rb') as f:
		dist = pickle.load(f)
	hist = {k: v._histogram for k, v in dist.items()} if isinstance(dist, dict) else dist._histogram
	print(f"Extracted histograms: {len(hist)}")
	hist_file = str(pkl_file).replace('dist', 'hist')
	print(f"dump histograms to {hist_file}")
	with open(hist_file, 'wb') as f:
		pickle.dump(hist, f, protocol=4, fix_imports=True)
	print("Finished")
