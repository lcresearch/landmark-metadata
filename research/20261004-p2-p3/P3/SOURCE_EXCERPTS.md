# P3 archived source statements

## F07-pinned-lite-card

Body SHA-256 `77300c8c37140316900b5712ad4c73f9dd2e87d0701c5804cdccf185b2b8bfae`. Line numbers refer to archived bytes.

```text
1: # Lite tensorflow/efficientnet/lite0/fp32/2
2: TF Lite deployment of tensorflow/efficientnet/lite0/classification/1.
3: 
4: <!-- asset-path: legacy -->
5: <!-- parent-model: tensorflow/efficientnet/lite0/classification/1 -->
6: <!-- interactive-visualizer: tflite_image_classifier -->
7: 
8: ## Description
```

## F10-pinned-parent-card

Body SHA-256 `2b94894d016a0b9a6edcb09d19d3e4b9a3d22ab5393c1af85c70d34a75511f58`. Line numbers refer to archived bytes.

```text
69: 
70: ```python
71: module = hub.Module("https://tfhub.dev/tensorflow/efficientnet/lite0/classification/1")
72: height, width = hub.get_expected_image_size(module)
73: images = ...  # A batch of images with shape [batch_size, height, width, 3].
74: logits = module(images)  # Logits with shape [batch_size, num_classes].
75: ```
76: 
77: ...or using the signature name `image_classification`. The indices into logits
78: are the `num_classes` = 1000 classes of the classification from the original
79: training (see above). The mapping from indices to class labels can be found in
80: the file at
81: [download.tensorflow.org/data/ImageNetLabels.txt](https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt)
82: and please ignore the first background class, ie. index 0 corresponds to
83: "tench".
```

## I02-publisher-doc

Body SHA-256 `09a1e137ea2d8be3295bc4704c86fb89f4d7c736d71acd8bf74430b9c704e377`. Line numbers refer to archived bytes.

```text
2845: <h3 id="efficientnet-lite0_model_recommended" data-text="EfficientNet-Lite0 model (recommended)" tabindex="-1">EfficientNet-Lite0 model (recommended)</h3>
2846: 
2847: <p>The EfficientNet-Lite0 model uses an EfficientNet architecture and was trained
2848: using <a href="https://www.image-net.org">ImageNet</a> to recognize 1,000 classes, such as
2849: trees, animals, food, vehicles, person etc. See the <a href="https://storage.googleapis.com/mediapipe-tasks/image_classifier/labels.txt">full
2850: list</a>
2851: of supported labels. EfficientNet-Lite0 is available as an int8 and float 32
2852: model. This model is recommended because it strikes a balance between latency
2853: and accuracy. It is both accurate and lightweight enough for many use cases.</p>
2854: 
2855: <table>
2856:   <thead>
```

## I11-tpu-imagenet-source

Body SHA-256 `63355e418b545831539d5a35f97fe288ebfa57710fae6fdee906bb9576a14855`. Line numbers refer to archived bytes.

```text
189:     # The labels will be in range [1,1000], 0 is reserved for background
190:     label = tf.cast(
191:         tf.reshape(parsed['image/class/label'], shape=[]), dtype=tf.int32)
192: 
193:     if not self.include_background_label:
194:       # Subtract 1 if the background label is discarded.
195:       label -= 1
196: 
197:     onehot_label = tf.one_hot(label, self.num_label_classes)
```

## I12-tensorflow-imagenet-mapping-source

Body SHA-256 `3307986bd71e1c5de4317f55f4230dcf2a080045cfa8ae4e06ce2ccabacd1b8f`. Line numbers refer to archived bytes.

```text
67: 
68:   Returns:
69:       labels_to_names: dictionary where keys are integers from to 1000
70:       and values are human-readable names.
71: 
72:   We retrieve a synset file, which contains a list of valid synset labels used
73:   by ILSVRC competition. There is one synset one per line, eg.
74:           #   n01440764
75:           #   n01443537
76:   We also retrieve a synset_to_human_file, which contains a mapping from synsets
77:   to human-readable names for every synset in Imagenet. These are stored in a
78:   tsv format, as follows:
79:           #   n02119247    black fox
80:           #   n02119359    silver fox
81:   We assign each synset (in alphabetical order) an integer, starting from 1
82:   (since 0 is reserved for the background class).
83: 
84:   Code is based on
85:   https://github.com/tensorflow/models/blob/master/research/inception/inception/data/build_imagenet_data.py#L463
86:   """
87: 
88:   # pylint: disable=g-line-too-long
89:   base_url = 'https://raw.githubusercontent.com/tensorflow/models/master/research/slim/datasets/'
90:   synset_url = '{}/imagenet_lsvrc_2015_synsets.txt'.format(base_url)
91:   synset_to_human_url = '{}/imagenet_metadata.txt'.format(base_url)
92: 
93:   filename, _ = urllib.request.urlretrieve(synset_url)
94:   synset_list = [s.strip() for s in open(filename).readlines()]
95:   num_synsets_in_ilsvrc = len(synset_list)
96:   assert num_synsets_in_ilsvrc == 1000
97: 
98:   filename, _ = urllib.request.urlretrieve(synset_to_human_url)
99:   synset_to_human_list = open(filename).readlines()
100:   num_synsets_in_all_imagenet = len(synset_to_human_list)
101:   assert num_synsets_in_all_imagenet == 21842
102: 
103:   synset_to_human = {}
104:   for s in synset_to_human_list:
105:     parts = s.strip().split('\t')
106:     assert len(parts) == 2
107:     synset = parts[0]
108:     human = parts[1]
109:     synset_to_human[synset] = human
110: 
```
