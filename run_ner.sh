#!/bin/bash
java -mx400m -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer -loadJarClassifier ner-eng-ie.crf-3-all2008.ser.gz -outputFormat slashTags -port 8888
