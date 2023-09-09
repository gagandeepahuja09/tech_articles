* It watches for the changes in the k8s API server.
* It also watches the nodes (virtual machines) too see which one is free.
* How is the node decided for a pod?
    * NodeAffinity
    * *Hard Constraints (Predicates: for filtering)*. Eg:
        * Memory requirements: node must have a memory of 4 GB.
        * nodeSelector: Node must have a label of SSD.
    * *Soft Constraints (Prioritis: for sorting)*: Eg:
        * Spreading: Nodes should have equal distribution of pods.
        * !Sick

    chosenNode = sort(filter(nodes))[0]