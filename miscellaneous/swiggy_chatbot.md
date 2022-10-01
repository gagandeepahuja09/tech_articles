* Chatbots help in solving the problem of taking customer queries and resolving them in an automated way.
* There is a kind of workflow. Eg: if order is spilled, then do this. if food is not cooked properly, do this.
* This is just a *decision-tree* running at the backend.
* We are taking a path depending on some control variables.
* We don't need some fancy NLP.
* At each stop, the customer is shown a valid set of child nodes as an option to proceed further.

* Building of decision tree:
    * We need some historical data backing it.
    * The common reasons of cancellation were gathered from the conversations with the customers.

**Key Decisions** 
* *Webview*: 
    * A webpage loading in the app. Allows much more iterations than an app.
    * This also saves engineering time, cost as we only need to build it on React.
* *Interacting with a fraud detection service*
* *Interacting with a refunds service*
* *Interacting with a notification service*
* The state management for the decision tree can be done in any database.
* There could be multiple sources like:
    * Insight and analytics team feeding the data to the service.
    * A maker-checker flow gets created for that.
    * Ops and product folks take action on that. (Self-serve).
* *Fallback: 3rd party agent chat*.
* Bot efficacy percentage: The percentage of conversations resolved by the bot vs the percentage of conversations resolved by the support executives.