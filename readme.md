## Discrete Representation of Time Series Data using VAE with Discrete Latent Variables

### Summary


### Todos 

Priority:
- enc, dec: 1d convolution, lstm
- implement 1 downstream task
- see if similar patches result in similar binary codes or
  - if similar binary codes corr. to similar patches
- normalize ts
- play with softmax temperature, number of bits
  - its ok if number of bits larger than patch length
- plot ts with real encodings

Nice to have

- piecewiese linear methods (e.g. PAA)
- additional "magnitude"+"shift" word? -> dependent on downstream tasks
- ensemble method to encode differnet attributes using differnt vaes
- generalization to other datasets
- Experiment management (wandb, mlflow)