# Doby
- NLP analysis and visualization of scholarly articles sourced from PubMed.
- Heroku deployment available at https://doby.herokuapp.com/ - it may take few seconds to load of the [dyno](https://www.heroku.com/dynos) is asleep. :sleeping:

---
#### Table of Contents
<!-- TABLE OF CONTENTS -->

<ol>
    	<li>
      <a href="#introduction">Introduction</a>
    	</li>
    	<li>
        	<a href="#flow-chart">Flow Chart</a>
    	</li>
    	<li>
	<a href="#content">Content</a>
	<ul>
		<li><a href="#home-page">Home Page</a></li>
		<li><a href="#search-page">Search Page</a></li>
	</ul>
    	</li>
    	<li>
	    <a href="#references">References</a>
	</li>
</ol>



<!-- Project Summary -->
## Introduction

Doby uses unigram, bigram and trigram frequency from the context of the searched articles, to help users understand the topic in a different point of view. It also provides a random thesis generator via Markov chain & Machine Learning and a convenient option of csv file export for trending articles and searched articles.


## Flow Chart

As can be seen in the following diagram, Doby uses Flask as the main web platform, and Heroku for PostgreSQL and deployment.


<img src="/doby screenshots/doby flowchart.png?raw=true" width="800px">

Packges utilized in Doby :

- Selenium and Beautiful Soup were used to access PubMed and to pull texts from available articles to be updated on the database.

- Nltk, spacy, re were used to clean out the text, and to remove stop words and unnecessary tokens.

- [**Markovify**](https://github.com/jsvine/markovify) was used for creating Markov Chain from the given text and its word tokens and to regenerate the sentence based on the # of states and word limits.

- Heroku chrome and chrome driver were also added as buildpacks for selenium on Heroku.

<img src="/doby screenshots/heroku chrome driver.png?raw=true" width="800px">
  


<!-- Progress -->
## Content

### Home Page
The home page includes the search bar, trending articles from PubMed, 'unigram, bigram, trigram' lists from the context, and option to export them as csv files.

<img src="/doby screenshots/indexhtml.png?raw=true" width="600px">
<img src="/doby screenshots/trendingarticles.png?raw=true" width="600px">
<img src="/doby screenshots/unigrams_t.png?raw=true" width="600px">
<img src="/doby screenshots/bigrams_t.png?raw=true" width="600px">
<img src="/doby screenshots/trigrams_t.png?raw=true" width="600px">
<img src="/doby screenshots/exportcsv.png?raw=true" width="600px">


### Search Page
The search page includes the queried keywords, auto sentence generator (refresh button), list of searched articles, 'unigram, bigram, trigram' from searched articles, and also an option to export the articles as csv files + a home button.


<img src="/doby screenshots/lemon and brain.png?raw=true" width="600px">
<img src="/doby screenshots/searchedarticles.png?raw=true" width="600px">
<img src="/doby screenshots/unigrams_s.png?raw=true" width="600px">
<img src="/doby screenshots/exportcsv_home.png?raw=true" width="600px">

---

### References
- [How to deploy your Flask app on Heroku](https://medium.com/@hannah.hj.do/deploy-flask-to-heroku-ed487041ac28)
- [Text Generation with Markov Chains: An Introduction to using Markovify](https://towardsdatascience.com/text-generation-with-markov-chains-an-introduction-to-using-markovify-742e6680dc33)



