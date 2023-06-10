* What is langchain and why do we need it?
* Helps to easily connect AI models/LLMs to outside sources.
* OpenAI doesn't want to build direct integrations with other sources.
* Why Langchain
    * Easy plug and play of LLMs.

* llm is a wrapper: ```from langchain.llms import OpenAI```

* **Quickstart Guide**
* temperature = 0 ==> no randomness.

* Langchain PromptTemplate object.
```
    prompt = PromptTemplate(
        input_variables=["food"],
        template="What are 5 vacation destinations for someone who likes to eat {food}",
    )
    print(llm(prompt))
```

**Agents**
* Chain run in a pre-determined order.
* Agents instead use an LLM to determine which actions to take and in what order.

**ChatModels**

**Custom Tools**