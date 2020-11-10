mkdir bpe
mkdir bpe/preprocessed_data
mkdir bpe/prepared_data

# learn a joint bpe model and vocab
subword-nmt learn-joint-bpe-and-vocab --input baseline/preprocessed_data/train.de baseline/preprocessed_data/train.en  -s 2000 --total-symbols -o bpe/bpe_model --write-vocabulary bpe/bpe_vocab.de bpe/bpe_vocab.en

# apply bpe to the German data
subword-nmt apply-bpe -c bpe/bpe_model --vocabulary bpe/bpe_vocab.de --vocabulary-threshold 1 < baseline/preprocessed_data/train.de > bpe/preprocessed_data/train.de
subword-nmt apply-bpe -c bpe/bpe_model --vocabulary bpe/bpe_vocab.de --vocabulary-threshold 1 < baseline/preprocessed_data/tiny_train.de > bpe/preprocessed_data/tiny_train.de
subword-nmt apply-bpe -c bpe/bpe_model --vocabulary bpe/bpe_vocab.de --vocabulary-threshold 1 < baseline/preprocessed_data/valid.de > bpe/preprocessed_data/valid.de
subword-nmt apply-bpe -c bpe/bpe_model --vocabulary bpe/bpe_vocab.de --vocabulary-threshold 1 < baseline/preprocessed_data/test.de > bpe/preprocessed_data/test.de

# apply bpe to the English data
subword-nmt apply-bpe -c bpe/bpe_model --vocabulary bpe/bpe_vocab.en --vocabulary-threshold 1 < baseline/preprocessed_data/train.en > bpe/preprocessed_data/train.en
subword-nmt apply-bpe -c bpe/bpe_model --vocabulary bpe/bpe_vocab.en --vocabulary-threshold 1 < baseline/preprocessed_data/tiny_train.en > bpe/preprocessed_data/tiny_train.en
subword-nmt apply-bpe -c bpe/bpe_model --vocabulary bpe/bpe_vocab.en --vocabulary-threshold 1 < baseline/preprocessed_data/valid.en > bpe/preprocessed_data/valid.en
subword-nmt apply-bpe -c bpe/bpe_model --vocabulary bpe/bpe_vocab.en --vocabulary-threshold 1 < baseline/preprocessed_data/test.en > bpe/preprocessed_data/test.en

# prepare the data
python preprocess.py --target-lang en --source-lang de --dest-dir bpe/prepared_data/ --train-prefix bpe/preprocessed_data/train --valid-prefix bpe/preprocessed_data/valid --test-prefix bpe/preprocessed_data/test --tiny-train-prefix bpe/preprocessed_data/tiny_train --threshold-src 1 --threshold-tgt 1 --num-words-src 1800 --num-words-tgt 1800
