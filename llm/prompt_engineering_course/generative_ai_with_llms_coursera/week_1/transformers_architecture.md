* RNNs were the most commonly used models for text generation before LLMs.
* They were quite CPU and memory intensive.
* They were not able to understand the meaning of the sentence.
* For each word, only the previous word was the neighbour.
* Scaling was a challenge with RNNs.

* Rather that learning the context of only the neighbour words, LLM is able to understand the context of every other word in the sentence.
    * We can visualize that each word has an edge with every other word rather that only neighbours.
    * Also called attention map.
* *Self-attention*: The LLM is able to understand the weights of the relation b/w the words. Eg sentence: The teacher taught the student with a book.
    * The work book is strong paying attention to the work teacher and student.
* *Simplified transformer diagram*: Encoder, Decoder.

* *What are embeddings in LLM context?*
* They are numerical representation of words or tokens.
* *Why do we need embeddings*
    1. *Semantic meaning*: Word with similar meaning tend to have similar embeddings.
* Before embedding, tokenization happens to get the numerical representation. Then embedding converts it into multi-dimensional vector.
* Word -> token_id -> vector
* Original vector paper ==> vector size was 512 ==> does that mean 512 dimensions?
* Apart from token embeddings, we also have position embeddings.

* Transformers run multiple sequences in parallel.

**BERT**
* BERT only consists of encoders while GPT-3 consists of only decoders.
* Input embedding for BERT
    * Positional encoding: passing the information of location of word to the transformer.
    * Segment or sentence encoding: Similar to positional but we are looking at the difference of first and second sentence.
    * Token encoding: Representation of each word in a numerical form.

* *How do you train the model to understand the meaning of the sentences and the core of the language?*
    * We are not trying to train in a single task.
    * BERT is trained on 2 different tasks: 
        * Masked Language Modeling
        * Next Sentence Prediction
* *Masked Language Modeling*: 15 percent of the tokens (not words) are left masked or blank. It is model's job to predict those tokens.
* *Next Sentence Prediction*: Training data has 2 sentences, it is model's job to predict whether they belong together. That is, should come after each other or not.

* *Fine-tuning BERT*
* You will need 2 things:
    * *New Output Layer*: plugged at the end of BERT for the specific task we are trying to perform.
    * *Dataset*: specific to the task you are trying to achieve.
* If we are doing sentiment analysis, we need a plugin an output layer of neurons after BERT. This will classify the output of BERT.
* During fine-tuning, the parameters of the output layer are updated. The parameters update in BERT are very minor.
    * BERT_base: 110M parameters, 12 layers of encoders
    * BERT_large: 340M parameters, 24 layers of encoders