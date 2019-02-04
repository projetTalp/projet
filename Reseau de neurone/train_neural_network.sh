#!/bin/bash

data_dir=.
train=$data_dir/dummy_train.csv
dev=$data_dir/dummy_dev.csv
test=$data_dir/dummy_test.csv
input=0,1
output=6
model_file=$data_dir/my_model.json
epochs=500
verbose=0

python train_neural_network.py --epochs $epochs \
                               --save-model $model_file \
                               --train-input $train:$input \
                               --train-output $train:$output \
                               --dev-input $dev:$input \
                               --dev-output $dev:$output \
                               --test-input $test:$input \
                               --test-output $test:$output

