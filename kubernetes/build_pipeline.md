* Having internal container registry.
* Pulling images from the registry. Through an admission controller, we can ensure that images are only pulled from a specific container registry (internal).
    * We are going to validate that the image always starts with a prefix. that is of the pattern: "myregistry.acr.io/*".
* Writing our own admission controller can be a little daunting.
    * *kubernetes policy controller*: easy to use implementation of one of these admission controller.
* Build pipeline: Source code to image.
    * No one apart from our build pipeline should have permissions to push images to our build registry.
    * We need to put both checks:
        * We can only deploy