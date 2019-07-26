{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "ename": "OSError",
     "evalue": "[E050] Can't find model 'en_core_web_md'. It doesn't seem to be a shortcut link, a Python package or a valid path to a data directory.",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mOSError\u001b[0m                                   Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-13-f77eb17bc4e9>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mspacy\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      2\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 3\u001b[0;31m \u001b[0mnlp\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mspacy\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mload\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m'en_core_web_md'\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[0;32m/usr/local/lib/python3.7/site-packages/spacy/__init__.py\u001b[0m in \u001b[0;36mload\u001b[0;34m(name, **overrides)\u001b[0m\n\u001b[1;32m     25\u001b[0m     \u001b[0;32mif\u001b[0m \u001b[0mdepr_path\u001b[0m \u001b[0;32mnot\u001b[0m \u001b[0;32min\u001b[0m \u001b[0;34m(\u001b[0m\u001b[0;32mTrue\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;32mFalse\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;32mNone\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     26\u001b[0m         \u001b[0mdeprecation_warning\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mWarnings\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mW001\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mformat\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mpath\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mdepr_path\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 27\u001b[0;31m     \u001b[0;32mreturn\u001b[0m \u001b[0mutil\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mload_model\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mname\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m**\u001b[0m\u001b[0moverrides\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     28\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     29\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m/usr/local/lib/python3.7/site-packages/spacy/util.py\u001b[0m in \u001b[0;36mload_model\u001b[0;34m(name, **overrides)\u001b[0m\n\u001b[1;32m    134\u001b[0m     \u001b[0;32melif\u001b[0m \u001b[0mhasattr\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mname\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m\"exists\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m  \u001b[0;31m# Path or Path-like to model data\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    135\u001b[0m         \u001b[0;32mreturn\u001b[0m \u001b[0mload_model_from_path\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mname\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m**\u001b[0m\u001b[0moverrides\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 136\u001b[0;31m     \u001b[0;32mraise\u001b[0m \u001b[0mIOError\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mErrors\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mE050\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mformat\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mname\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mname\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    137\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    138\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mOSError\u001b[0m: [E050] Can't find model 'en_core_web_md'. It doesn't seem to be a shortcut link, a Python package or a valid path to a data directory."
     ]
    }
   ],
   "source": [
    "import spacy\n",
    "\n",
    "nlp = spacy.load('en_core_web_md')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/usr/local/lib/python3.7/runpy.py:193: ModelsWarning: [W007] The model you're using has no word vectors loaded, so the result of the Doc.similarity method will be based on the tagger, parser and NER, which may not give useful similarity judgements. This may happen if you're using one of the small models, e.g. `en_core_web_sm`, which don't ship with word vectors and only use context-sensitive tensors. You can always add your own word vectors, or use one of the larger models instead if available.\n",
      "  \"__main__\", mod_spec)\n",
      "/usr/local/lib/python3.7/runpy.py:193: ModelsWarning: [W007] The model you're using has no word vectors loaded, so the result of the Doc.similarity method will be based on the tagger, parser and NER, which may not give useful similarity judgements. This may happen if you're using one of the small models, e.g. `en_core_web_sm`, which don't ship with word vectors and only use context-sensitive tensors. You can always add your own word vectors, or use one of the larger models instead if available.\n",
      "  \"__main__\", mod_spec)\n",
      "/usr/local/lib/python3.7/runpy.py:193: ModelsWarning: [W007] The model you're using has no word vectors loaded, so the result of the Doc.similarity method will be based on the tagger, parser and NER, which may not give useful similarity judgements. This may happen if you're using one of the small models, e.g. `en_core_web_sm`, which don't ship with word vectors and only use context-sensitive tensors. You can always add your own word vectors, or use one of the larger models instead if available.\n",
      "  \"__main__\", mod_spec)\n",
      "/usr/local/lib/python3.7/runpy.py:193: ModelsWarning: [W007] The model you're using has no word vectors loaded, so the result of the Doc.similarity method will be based on the tagger, parser and NER, which may not give useful similarity judgements. This may happen if you're using one of the small models, e.g. `en_core_web_sm`, which don't ship with word vectors and only use context-sensitive tensors. You can always add your own word vectors, or use one of the larger models instead if available.\n",
      "  \"__main__\", mod_spec)\n",
      "/usr/local/lib/python3.7/runpy.py:193: ModelsWarning: [W007] The model you're using has no word vectors loaded, so the result of the Doc.similarity method will be based on the tagger, parser and NER, which may not give useful similarity judgements. This may happen if you're using one of the small models, e.g. `en_core_web_sm`, which don't ship with word vectors and only use context-sensitive tensors. You can always add your own word vectors, or use one of the larger models instead if available.\n",
      "  \"__main__\", mod_spec)\n",
      "/usr/local/lib/python3.7/runpy.py:193: ModelsWarning: [W007] The model you're using has no word vectors loaded, so the result of the Doc.similarity method will be based on the tagger, parser and NER, which may not give useful similarity judgements. This may happen if you're using one of the small models, e.g. `en_core_web_sm`, which don't ship with word vectors and only use context-sensitive tensors. You can always add your own word vectors, or use one of the larger models instead if available.\n",
      "  \"__main__\", mod_spec)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "They  -  Sally , similarity:  0.3557482477404074\n",
      "They  -  likes , similarity:  0.14822688003661538\n",
      "They  -  savory , similarity:  0.21891309099484121\n",
      "They  -  cakes , similarity:  0.17339725708516612\n",
      "sell  -  Sally , similarity:  0.19820034055150304\n",
      "sell  -  likes , similarity:  0.3575345116086287\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/usr/local/lib/python3.7/runpy.py:193: ModelsWarning: [W007] The model you're using has no word vectors loaded, so the result of the Doc.similarity method will be based on the tagger, parser and NER, which may not give useful similarity judgements. This may happen if you're using one of the small models, e.g. `en_core_web_sm`, which don't ship with word vectors and only use context-sensitive tensors. You can always add your own word vectors, or use one of the larger models instead if available.\n",
      "  \"__main__\", mod_spec)\n",
      "/usr/local/lib/python3.7/runpy.py:193: ModelsWarning: [W007] The model you're using has no word vectors loaded, so the result of the Doc.similarity method will be based on the tagger, parser and NER, which may not give useful similarity judgements. This may happen if you're using one of the small models, e.g. `en_core_web_sm`, which don't ship with word vectors and only use context-sensitive tensors. You can always add your own word vectors, or use one of the larger models instead if available.\n",
      "  \"__main__\", mod_spec)\n",
      "/usr/local/lib/python3.7/runpy.py:193: ModelsWarning: [W007] The model you're using has no word vectors loaded, so the result of the Doc.similarity method will be based on the tagger, parser and NER, which may not give useful similarity judgements. This may happen if you're using one of the small models, e.g. `en_core_web_sm`, which don't ship with word vectors and only use context-sensitive tensors. You can always add your own word vectors, or use one of the larger models instead if available.\n",
      "  \"__main__\", mod_spec)\n",
      "/usr/local/lib/python3.7/runpy.py:193: ModelsWarning: [W007] The model you're using has no word vectors loaded, so the result of the Doc.similarity method will be based on the tagger, parser and NER, which may not give useful similarity judgements. This may happen if you're using one of the small models, e.g. `en_core_web_sm`, which don't ship with word vectors and only use context-sensitive tensors. You can always add your own word vectors, or use one of the larger models instead if available.\n",
      "  \"__main__\", mod_spec)\n",
      "/usr/local/lib/python3.7/runpy.py:193: ModelsWarning: [W007] The model you're using has no word vectors loaded, so the result of the Doc.similarity method will be based on the tagger, parser and NER, which may not give useful similarity judgements. This may happen if you're using one of the small models, e.g. `en_core_web_sm`, which don't ship with word vectors and only use context-sensitive tensors. You can always add your own word vectors, or use one of the larger models instead if available.\n",
      "  \"__main__\", mod_spec)\n",
      "/usr/local/lib/python3.7/runpy.py:193: ModelsWarning: [W007] The model you're using has no word vectors loaded, so the result of the Doc.similarity method will be based on the tagger, parser and NER, which may not give useful similarity judgements. This may happen if you're using one of the small models, e.g. `en_core_web_sm`, which don't ship with word vectors and only use context-sensitive tensors. You can always add your own word vectors, or use one of the larger models instead if available.\n",
      "  \"__main__\", mod_spec)\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "sell  -  savory , similarity:  0.38560386490450915\n",
      "sell  -  cakes , similarity:  0.3600760672469081\n",
      "sweet  -  Sally , similarity:  0.32533533793658004\n",
      "sweet  -  likes , similarity:  0.18247615849323476\n",
      "sweet  -  savory , similarity:  0.42969144128642534\n",
      "sweet  -  cakes , similarity:  0.1034686835015707\n",
      "candies  -  Sally , similarity:  0.29375694878155917\n",
      "candies  -  likes , similarity:  0.6105909113428374\n",
      "candies  -  savory , similarity:  0.366014966352005\n",
      "candies  -  cakes , similarity:  0.8021860432229484\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/usr/local/lib/python3.7/runpy.py:193: ModelsWarning: [W007] The model you're using has no word vectors loaded, so the result of the Doc.similarity method will be based on the tagger, parser and NER, which may not give useful similarity judgements. This may happen if you're using one of the small models, e.g. `en_core_web_sm`, which don't ship with word vectors and only use context-sensitive tensors. You can always add your own word vectors, or use one of the larger models instead if available.\n",
      "  \"__main__\", mod_spec)\n",
      "/usr/local/lib/python3.7/runpy.py:193: ModelsWarning: [W007] The model you're using has no word vectors loaded, so the result of the Doc.similarity method will be based on the tagger, parser and NER, which may not give useful similarity judgements. This may happen if you're using one of the small models, e.g. `en_core_web_sm`, which don't ship with word vectors and only use context-sensitive tensors. You can always add your own word vectors, or use one of the larger models instead if available.\n",
      "  \"__main__\", mod_spec)\n",
      "/usr/local/lib/python3.7/runpy.py:193: ModelsWarning: [W007] The model you're using has no word vectors loaded, so the result of the Doc.similarity method will be based on the tagger, parser and NER, which may not give useful similarity judgements. This may happen if you're using one of the small models, e.g. `en_core_web_sm`, which don't ship with word vectors and only use context-sensitive tensors. You can always add your own word vectors, or use one of the larger models instead if available.\n",
      "  \"__main__\", mod_spec)\n",
      "/usr/local/lib/python3.7/runpy.py:193: ModelsWarning: [W007] The model you're using has no word vectors loaded, so the result of the Doc.similarity method will be based on the tagger, parser and NER, which may not give useful similarity judgements. This may happen if you're using one of the small models, e.g. `en_core_web_sm`, which don't ship with word vectors and only use context-sensitive tensors. You can always add your own word vectors, or use one of the larger models instead if available.\n",
      "  \"__main__\", mod_spec)\n"
     ]
    }
   ],
   "source": [
    "string1 = 'They sell sweet candies'\n",
    "string2 = 'Sally likes savory cakes'\n",
    "for word1 in string1.split(' '):\n",
    "    for word2 in string2.split(' '):\n",
    "        #print(word1)\n",
    "        print(nlp(word1), ' - ', nlp(word2), ', similarity: ', nlp(word1).similarity(nlp(word2)))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
