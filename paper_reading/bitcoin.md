**Abstract**
* Allow online payments to be sent from one party to another without the involvement of financial institution.
* Why is this a problem: double spending: we can easily create duplicates and then send the token.
* Digital signature (cryptography) provide part of the solution. It is a way to judge whether the information is coming from a genuine source or not.
    * A user has its own private key and public key. as name suggests, private key will only be with me while the public key can distributed to the whole world.
    * Public key is used only for verification purposes while private key is used for creation purpose.
    * Eg: we can verify if a user X is the owner of some entity.
* Digital signature alone cannot solve the problem of double spending. We can ensure that A is send to B but cannot ensure that A is not double spending before sending.
* There won't be any central entity. It will be a pure P2P network.
* In regular cases, we have trust the bank that they will be performing the transactions in a non-fraudulent manner. We could still see some frauds or scams. We are also subject to various problems like bank and gateway fees, inflation, currency changes, etc.
* Bittorent and early internet were P2P.

**Introduction**
* In electronic cash, reversal of transactions should not be possible. We should rather initiate a reverse transaction.
* Privacy of a user is compromised in bank transactions as the bank requires a lot of data points like SSN, adhaar, etc to establish trust with the customer.

**Transactions**
* Private keys are gigantic. It would take hundreds and thousands of years to guess the private key of a person.
* Electric coin is defined as a *chain of digital signatures*.
* Each owner transfers the coin to the next by digitally signing a hash of the previous transaction and the public key of the next owner and adding these to the end of the coin. This will act as a ledger indicating how the ownership transferred from one user to the other.
* In this approach, how do we know that the previous owner did not sign any other transactions?
* If A sends money to B, then B (payee) needs to be sure that the money was not double spent.
    * The payee needs proof that at the time of transaction, the majority of nodes agreed it was the first received.

**Timestamp Server**
* Rather than a bank transaction where everything is confidential and no one is aware of anyone else's transactions, in case of bitcoin, since it is a P2P network, the hash along with the timestamp is published to the entire audience.

27:58
**Proof Of Work**
* Nonce: It is like an OTP.


*********************************************************************************************

https://www.youtube.com/watch?v=bBC-nXj3Ng4

* Ledger - Trust + Cryptography = Cryptocurrency

**Digital Signatures**
* Communal ledger ==> based on trust.
* How to verify that A sent money to B. Anyone can go ahead and write in the ledger.
    * We can use digital signatures.
    * But can't we copy the signatures as it would similar to text.
    * In digital signatures, everyone generates a public and private (secret) key.
    * Both of them are just pair of 1s and 0s.
    * We can change the pair for different transactions.
* Signing of Signatures:
    * Sign(Message, sk) = Signature
    * Private key ensures that only the owner can produce the signature.
    * Since each message would also be unique, no one can copy the signature and then make use of it for forging other messages.
* Verification of Signature:
    * This is where the public key comes in.
    * A signature is of 256 bit ==> 2 ^ 256 possibilities.
    * Verify(Message, 256 bit signature, pk) = T/F.
* **Unique Id, Timestamp Server**: The problem of double spending is still not solved as someone can just duplicate a valid transaction. We need to ensure that each message needs to have a unique id associated with transaction. This is generally done via timestamp server? 
    * Since message changes, the signature also changes.

**Settlements**
* We just maintain a ledger and settle up each month.
* But how do we establish trust in that case, a person could just run away and refuse to give the money.
* In order to solve for the problem, we can ensure that no one is overspending (spending more than they already have).
* Everyone needs to deposit some money in the pot and can never take more than the money deposited.
* This means that verifying a transaction requires knowing the fully history of the transactions till that point.

**Decentralization**
* Who owns and hosts the website? Who will have the control of adding new lines in the ledger.
* Everyone needs to keep their own copy of the ledger.
* How to get everyone to agree on what is the right ledger?

**Proof Of Work**
* Whichever ledger has the most computational work put into it.
* Fraudulent transaction would be computationally infeasible.
* How to prove that a list of transactions is associated with a large amount of computational effort.

**Cryptographic Hash Functions**
* Eg. SHA256 ==> output will be 256 random bits. There is no computational relation b/w the input and the output. You can decode and get the input from the output.
* Even if we change a single character of the input, the output completely changes.
* A lot of modern security depends on cryptographic functions but there is no theoretical proof that the inverse is impossible (we just agree that it is computationally infeasible).