

import random
numberOfNodes = 100
numberOfLinks = 300

width = 800
height = 800

nodes = []
links = []

for i in range(numberOfNodes) :
    node = {}
    node['id'] = i
    node['x'] = random.randrange(0,width)
    node['y'] = random.randrange(0,height)
    nodes.append(node)
    
for i in range(numberOfLinks) :
    link = {}
    link['source'] = random.randrange(0,numberOfNodes)
    link['target'] = random.randrange(0,numberOfNodes)
    links.append(link)
    
