# Probability Sampling for Mastodon Instances

This repository contains documentation for an approach akin to to random digit dialing (RDD) for phone surveys. 

**Observation** Many Mastodon instances we identified used the `.social` or `.local` domain suffix. We are going to attempt to generate random domains that use that suffix and test whether they correspond to Mastodon servers. 

**Why do this?** Classically, random digit dialing was used for probability sampling for surveys. Probability sampling methods allow researchers to collect _unbiased_ samples from a population of interest. Since there is no canonical list of all Mastodon servers, performing probability sampling is much harder. An approach that approximates random digit dialing could help.

_Threat to validity: extension semantics_ It is possible that administrators who register their domains with the suffix `.social` differ in some systematic way from the general population of Mastodon administrators. This difference is only an issue if it will bias our findings; for example, perhaps administrators use `.social` because they are trying to grow their communities and take a more liberal posture towards privacy. Since we are using two other sampling methods, we will compare between the samples derived using the other methods to see if there are substantial differences we should consider. 

## Method

Our method uses the following procedure:

1. Identify or generate a list of possible domain base names 
2. For each of a list of extensions commonly seen associated with social servers (e.g., `.social`, `.local`, `.club`, etc.), query `https://{BASE}.{EXT}/`
3. Filter for the domains that appear to be running Mastodon. 
4. Exclude domains we have already contacted via other means.

Since we are interested in English-language servers, we started with a some lists of English language words. You can find these in the folder `{REPO_HOME}/mastodon/collect/rdd/words`:

* **[sgb-words.txt](https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt)** Donald Knuth's list of 5,757 5-letter words.
* **[common-6.txt](http://www.poslarchive.com/math/scrabble/lists/common-6.html)** A list of 15,788 common 6-letter words. 
* **[seven-letters.txt](https://github.com/powerlanguage/word-lists/blob/master/common-7-letter-words.txt)** A list of 500 7-letter words. 

As a point of reference, we also have a list of 5,757 5-letter "words" consisting of random letters and numbers. These were produced using the script in `{REPO_HOME}/mastodon/rdd/wordgen/get_5char_words.py`

## Usage

You can see basic instructions for how to generate the list of domains by calling the program with the `-h` flag:

`(.venv)> python -m mastodon.instances.rdd -h`

The minimum required argument is a file name that contains the list of words you want to use as the base domain name. 

