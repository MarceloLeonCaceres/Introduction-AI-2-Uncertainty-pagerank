import os
import random
import re
import sys
from typing import Counter
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])    
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    
    # begin of modifications
    # enumerate and print each of the pages and links   
    # print(f"Total páginas = {len(corpus)}") 
    # for key, value in corpus.items():
    #     print(f"pagina: {key}, links: {value}, NumLinks= {len(value)}")        
    #transition_model(corpus, 'ai.html', DAMPING)
    # end of modifications

    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    distribution = dict()
    N = len(corpus)
    NumLinks = len(corpus[page])
    # print(f"NumLinks = {NumLinks}")
    if NumLinks == 0:
        for key, value in corpus.items():
            distribution[key] = 1/N
    else:
        for key, value in corpus.items():
            if(key in corpus[page]):    
                distribution[key] = (1-DAMPING)/N + DAMPING/NumLinks
            else:
                distribution[key] = (1-DAMPING)/N

    # Probability distribution
    #for key, value in distribution.items():
    #    print(f"pagina: {key}, probabilidad: {value}")
    return distribution 
    # raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    samplingRank = dict()
    for key, value in corpus.items():
        samplingRank[key] = 0    
    paginaInicial = random.choice(list(corpus))
    samplingRank[paginaInicial] += 1
    #print(f"La página inicial fue: {paginaInicial}")
    for i in range(n):
        paginaSiguiente = random.choices(list(corpus), 
                                        weights=list(transition_model(corpus, paginaInicial, damping_factor).values()), 
                                        k=1)[0]
        #print(f"La página siguiente fue: {paginaSiguiente}")
        samplingRank[paginaSiguiente] += 1
        paginaInicial = paginaSiguiente
    
    for key, value in samplingRank.items():
        samplingRank[key] = samplingRank[key] / (n+1)   
    return samplingRank
    #raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    print("Begin iterative PageRank algorithm")
    initialRank = dict()
    pageRank = dict()
    N = len(corpus)
    
    for key, value in corpus.items():
        initialRank[key] = 1/N
    
    corpusCopy = copy.deepcopy(corpus)
    maximo = 1
    i = 0
    while maximo > 0.005:
    #for i in range(10):
        maximo = 0.0
        for pageP, value in corpusCopy.items():        
            sumatoria = 0
            for page_i, lista_i in corpus.items():            
                if(pageP in lista_i):
                    sumatoria += initialRank[page_i]/ len(lista_i)
            pageRank[pageP] = ((1 - damping_factor)/N) + (damping_factor * sumatoria)
            #print(f"{i}: pageRank[pageP] - initialRank[pageP]: {pageRank[pageP]:.4f} - {initialRank[pageP]:.4f} len: {len(pageRank)} {len(initialRank)}")
            maximo += abs(pageRank[pageP] - initialRank[pageP])
            #print(f"pageRank[pageP] - initialRank[pageP] {pageRank[pageP]:.4f}  {initialRank[pageP]:.4f}")

        # print(f"maximo= {maximo:.4f}")
        # for page, value in corpus.items():
        #     print(f"initialRank[page] - pageRank[page] {initialRank[page]:.4f}  {pageRank[page]:.4f}")
        #     maximo += abs(initialRank[page] - pageRank[page])
        #     print(f"maximo= {maximo:.4f}")
        i+=1
        if(maximo < 0.005):
            print(f"The target was reached (diff={maximo:.4f} < 0.005) in {i} iterations")
        
        initialRank = copy.deepcopy(pageRank)
        
    return initialRank
    # raise NotImplementedError


if __name__ == "__main__":
    main()
