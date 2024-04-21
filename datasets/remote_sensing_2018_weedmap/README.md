---
dataset_info:
- config_name: red_edge
  features:
  - name: B
    dtype: image
  - name: CIR
    dtype: image
  - name: G
    dtype: image
  - name: NDVI
    dtype: image
  - name: NIR
    dtype: image
  - name: R
    dtype: image
  - name: RE
    dtype: image
  - name: RGB
    dtype: image
  - name: annotation
    dtype: image
  splits:
  - name: train
    num_bytes: 1180504
    num_examples: 766
  - name: test
    num_bytes: 314394
    num_examples: 204
  download_size: 637901163
  dataset_size: 1494898
- config_name: sequoia
  features:
  - name: CIR
    dtype: image
  - name: G
    dtype: image
  - name: NDVI
    dtype: image
  - name: NIR
    dtype: image
  - name: R
    dtype: image
  - name: RE
    dtype: image
  - name: annotation
    dtype: image
  splits:
  - name: train
    num_bytes: 515690
    num_examples: 428
  - name: test
    num_bytes: 327726
    num_examples: 272
  download_size: 444145925
  dataset_size: 843416
---
