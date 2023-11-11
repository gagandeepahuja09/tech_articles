**Deep Learning**
* An approach to ML characterized by deep stacks of computation.
* This depth of computation enables deep learning models to entangle the complex and hierarichal patterns found in most challenging real-world datasets.
* *Neural networks*: 
    * Defining model of deep learning.
    * Composed of neurons where each neuron individually performs only a single computation.

**Neuron: The Linear Unit**
* y = wx + b
* x => input, y => output
* Special kind of weight which doesn't have any input associated with it.

**Example: Linear unit as a model**
* x = sugar, y = calories

**Multiple Inputs**
* More features than just sugar: eg. fibre or protein content.
* y = w0x0 + w1x1 + w2x2 + b
* keras.Sequential: creates a neural network as a stack of layers.

`
    from tensorflow import keras
    from tensorflow.keras import layers

    model = keras.Sequential([
        layers.Dense(units=1, input_shape=[3])
    ])
    # where do we mention that the 3 features are sugars, fibre, protein? we have only told the count.
    # where is the target column mentioned?
`
* We can see the weights and biases assigned via `model.weights`.

**Plotting the output: Untrained model**
* Untrained: weights would be set randomly.
* Regression problems are like "curve-fitting". We try to find a curve that best fits the data.

`
    import tensorflow as tf
    import matplotlib.pyplot as plt

    model = keras.Sequential([
        layers.Dense(1, input_shape=[1]),
    ])

    x = tf.linspace(-1.0, 1.0, 100)
    y = model.predict(x)

    plt.figure, plot, xlabel, ylabel, xlim, ylim, title, show
`