# Probability Sampling for Mastodon instances

This repository contains documentation for an approach akin to to random digit dialing (RDD) for phone surveys. 

**Observation** Many Mastodon instances we identified used the `.social` or `.local` domain suffix. We are going to attempt to generate random domains that use that suffix and test whether they correspond to Mastodon servers. 

**Why do this?** Classically, random digit dialing was used for probability sampling for surveys. Probability sampling methods allow researchers to collect _unbiased_ samples from a population of interest. Since there is no canonical list of all Mastodon servers, performing probability sampling is much harder. An approach that approximates random digit dialing could help.

_Threat to validity: extension semantics_ It is possible that administrators who register their domains with the suffix `.social` differ in some systematic way from the general population of Mastodon administrators. This difference is only an issue if it will bias our findings; for example, perhaps administrators use `.social` because they are trying to grow their communities and take a more liberal posture towards privacy. Since we are using two other sampling methods, we will compare between the samples derived using the other methods to see if there are substantial differences we should consider. 

# Method

Our method uses the following procedure:

1. Identify or generate a list of possible domain names 
2. Ping the name with the `.social` extension and log the domains that return at least one packet in response.
3. Filter for the domains that appear to be running Mastodon. 

Since we are interested in English-language servers, we started with a list of English language words. To keep things simple, we used the list of 5,757 5-letter words from Donald Knuth. 