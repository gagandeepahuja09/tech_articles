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
* *Why do we need padding?*
    * If we use many such layers in a neural network, it is possible that the final size of the *image gets reduced* by so much that we might loose the valuable information.
    * The corner pixel are not getting exposed multiple times by the filter.
    * *Solution*: Pad the image with a border of 0s. We can also increase the width of padding by adding more borders.
* *Why f is an odd number*
    * To cover the input matrix and ensure the elements are exposed more equally.
    * If we use f as odd, we would require doing assymetric padding.
(2:32 or 4:09)
