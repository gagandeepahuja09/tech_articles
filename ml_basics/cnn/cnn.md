https://www.youtube.com/playlist?list=PLuhqtP7jdD8CD6rOWy20INGM44kULvrHu
# Convolution Operation in CNN
* **What is a convolution operation (*)**
* Visualize an image as a matrix. Each value denotes the pixel value.
* In case of a black and white image, each value would be between 0 and 255. 0 ==> black, 255 ==> white.
* (**Question: why 0 to 255?**)
* Why a 3 * 3 pixel?
    * Odd number helps, how?
    * Values are [[1, 0, -1], [1, 0, -1], [1, 0, -1]]. ==> Vertical edge detector.
        * How did we come to know that these are appropriate values?
* We super-impose the filter on the image and use it as a sliding window.

* *Example: vertical edge detector*
* Assume 1 => white, 0 => grey
*   [ 1, 1, 1, 0, 0, 0]
    [ 1, 1, 1, 0, 0, 0]
    [ 1, 1, 1, 0, 0, 0]
    [ 1, 1, 1, 0, 0, 0]
    [ 1, 1, 1, 0, 0, 0]
* Above matrix denotes a vertical line. Our filter/kernel will help us find out the vertical edge.
* Horizontal edge detector ==> [[1, 1, 1], [0, 0, 0], [-1, -1, -1]]
* Convolution operation acts as the feature detector.
* In a single layer of CNN, we would be using many such filters.
* If we use c such filters, the resultant output will have c such images.
    * Image size = (n * n * 1)
    * c Filters = (f * f * c)
    * Ouput c images ==> (n - f + 1) * (n - f + 1) * c

* **Convolution operation for colored image**
* Image size = (n * n * 3) ==> for 3 channels ==> R, G, B
* Filter size ==> (f * f * 3)
* Output of 1 image ==> (n - f + 1) * (n - f + 1)
* We superimposed and multiplied 27 values in this case.

# Padding
* If we use a 3 * 3 filter, the size of the image gets reduced by an amount of 2.
* (**Question: why do we need an overlap and need to go through a single cell or pixel multiple times?**)
    * Is it for gradient descent / back propagation?
* *Why do we need padding?*
    * If we use many such layers in a neural network, it is possible that the final size of the *image gets reduced* by so much that we might loose the valuable information.
    * The corner pixel are not getting exposed multiple times by the filter.
    * *Solution*: Pad the image with a border of 0s. We can also increase the width of padding by adding more borders.
* *Why f is an odd number*
    * To cover the input matrix and ensure the elements are exposed more equally.
    * If we use f as odd, we would require doing assymetric padding.
* *Valid padding:* No padding.
* *Same padding*: Output image has the same size as input image.
    * Input image size = n + 2 * p = n'
    * Output image size = n = n' - f + 1
    * n + 2 p - f + 1 = n
    * p = (f - 1) / 2

# Stride
* We can slide the window by more than 1. The amount by which we slide the window is the stride value. This also reduces the output matrix size.
* If the input matrix is n1 * n2, output matrix = floor((n1 - f) / s + 1) * floor((n2 - f) / s + 1)
* If we are also using padding, formula changes to: floor((n1 + 2p - f) / s + 1) * floor((n2 + 2p - f) / s + 1)

# Max Pooling Layer
* The function of the pooling layers is to reduce the size or dimension of the image while preserving the features in it.
* Usually stride is taken the same as the filter length.
* **Max pooling example**

[
    [8, 1, 3, 6],
    [3, 2, 2, 1],
    [5, 0, 7, 1],
    [2, 4, 9, 7],
]

* Filter size = 2, Stride = 2
* Output = [
    [8, 6],
    [5, 9],
]

* **Why max pooling**
* Reduces the image, thus reduces computational cost.
* Features are not just preserved but also enhanced in many cases.
* Max pooling layer is always applied after the convolutional layer. So, this is the end layer after we have performed the convolution operation for reducing the image size and enhancing the features.
* It is upto us if we want to add a max pooling layer after a convolutional layer.
* It is a simple transformation operation and no training operations are involved here.
* Same number of channels in output as input.