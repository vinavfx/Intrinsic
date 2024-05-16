# Intrinsic for Nuke
Ported to Nuke [![ported](https://img.shields.io/badge/by:_Francisco_Contreras-blue?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/francisco-contreras-cuevas/)
#### Limitations:
1. It works very poorly for movement since it blinking too much.
2. It works poorly for very strong intensities and very marked shadows like that of the sun.


# Intrinsic Image Decomposition via Ordinal Shading
Code for the paper: Intrinsic Image Decomposition via Ordinal Shading, [Chris Careaga](https://ccareaga.github.io/) and [Yağız Aksoy](https://yaksoy.github.io), ACM Transactions on Graphics, 2023
### [Project Page](https://yaksoy.github.io/intrinsic) | [Paper](https://yaksoy.github.io/papers/TOG23-Intrinsic.pdf) | [Video](https://www.youtube.com/watch?v=pWtJd3hqL3c) | [Supplementary](https://yaksoy.github.io/papers/TOG23-Intrinsic-Supp.pdf) | [Data](https://github.com/compphoto/MIDIntrinsics)

We propose a method for generating high-resolution intrinsic image decompositions, for in-the-wild images. Our method relies on a carefully formulated ordinal shading representation, and real-world supervision from multi-illumination data in order to predict highly accurate albedo and shading. 

[![YouTube Video](./figures/thumbnail.jpg)](https://www.youtube.com/watch?v=pWtJd3hqL3c)


Try out our pipeline on your own images! [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/compphoto/Intrinsic/blob/main/intrinsic_inference.ipynb)

## Method
The inherently under-constrained and scale-invariant nature of the intrinsic decomposition makes it a challenging problem. 
Shading, which represents complex interactions in the scene, is difficult for neural networks to predict. 
Compounded by the scarcity of dense ground-truth data, state-of-the-art models fail at high resolutions in real-world scenarios.

![intro_itw_comp_avo](./figures/intro_itw_comp_avo.png)

Our method focuses on generating high-resolution shading estimations, rather than attempting to estimate shading and albedo separately. 
Since shading values are unbounded, we develop a representation of shading values called "inverse shading" which maps the shading values into the zero-one range.
This creates a balanced distribution of values in a well-defined range that is desirable for training neural networks.

![ordinal_shd_rep](./figures/ordinal_shd_rep.jpg)

Rather than directly regressing the inverse shading values, we relax the problem and aim to predict *ordinal* shading values.
To do this, we train our network using shift- and scale-invariant loss functions. 
This simplifies the task of shading estimation as the model does not need to estimate precise values that satisfy the core intrinsic decomposition model

![ord_behavior_itw](./figures/ord_behavior_itw.png)

Our ordinal estimations exhibit specific behaviors at different resolutions. 
At low resolutions, the model can generate globally coherent predictions, but the outputs lack details.
At high resolutions, the model can predict fine local details, but at the cost of global coherency. 

![pool_table](./figures/pool_table.png)

To generate a final shading estimation we combine two ordinal estimations, at low and high resolutions, with the input image and send them through a second network.
We use the final shading estimation, and the input image in order to compute our estimated albedo. This allows us to compute losses on both shading and albedo while
using only a single network.

![network_pipeline_circles](./figures/network_pipeline_circles.jpg)

We train our method on multiple rendered datasets. In order to generate real-world supervision for our method we use multi-illumination data. 
Using our pipeline we estimate the albedo for each image in a given multi-illumination scene. By taking the median across these albedo estimations, small errors are removed resulting in a single accurate albedo.
We use these 25,000 pseudo-ground-truth pairs as training data and continue training our pipeline.

![multi_illum_examples](./figures/multi_illum_examples.png)

Our method can be used for complex image editing tasks such as recoloring and relighting

![yellow_chair](./figures/yellow_chair.png)


## Installation
1. Download and unzip the latest release from [here](https://drive.google.com/file/d/1NXzWSENM20l2-52ewesyZQoQhvRXw0XC/view?usp=sharing).
2. Copy the extracted Cattery folder to .nuke or your plugins path.

## Compile
```sh
# Linux
git clone https://github.com/vinavfx/Intrinsic-for-Nuke.git
cd ./Intrinsic-for-Nuke

conda create -n intrinsic python=3.9
conda activate intrinsic
pip install .

wget https://github.com/compphoto/Intrinsic/releases/download/v1.0/final_weights.pt
python ./intrinsic_nuke.py
# Convert with CatFileCreator.nk
````

## Citation

```
@ARTICLE{careagaIntrinsic,
  author={Chris Careaga and Ya\u{g}{\i}z Aksoy},
  title={Intrinsic Image Decomposition via Ordinal Shading},
  journal={ACM Trans. Graph.},
  year={2023},
}
```

## License

This implementation is provided for academic use only. Please cite our paper if you use this code or any of the models. 

The methodology presented in this work is safeguarded under intellectual property protection. For inquiries regarding licensing opportunities, kindly reach out to SFU Technology Licensing Office &#60;tlo_dir <i>ατ</i> sfu <i>δøτ</i> ca&#62; and Dr. Yağız Aksoy &#60;yagiz <i>ατ</i> sfu <i>δøτ</i> ca&#62;.
