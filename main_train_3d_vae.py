import os
from config import *
#import setGPU
import numpy as np

import util.experiment as ex
import inout.input_data_reader as idr
from vae.vae_3Dloss_model import VAE_3D

# ********************************************************
#       runtime params
# ********************************************************

run_n = 2
experiment = ex.Experiment( run_n, model_dir=True )


# ********************************************************
#       read in training data ( events )
# ********************************************************

data_reader = idr.InputDataReader( os.path.join( config['input_dir'], 'background_small.h5' ))
train_evts_j1, train_evts_j2 = data_reader.read_jet_constituents( )
train_evts_j1, train_evts_j2 = np.expand_dims(train_evts_j1,axis=3), np.expand_dims(train_evts_j2,axis=3) # expand to channel dimension for convolution to [ batch-size x 100 x 3 x 1 ]

# ********************************************************
#       prepare training data
# ********************************************************

training_evts = np.vstack([train_evts_j1, train_evts_j2])
np.random.shuffle( training_evts )

# *******************************************************
#                       build model
# *******************************************************

vae = VAE_3D(run=run_n,model_dir=experiment.model_dir)
vae.build()

# *******************************************************
#                       train and save
# *******************************************************

vae.fit( training_evts, training_evts, epochs=10, verbose=2 )
vae.save_model( run_n )