import numpy
from numpy import linalg
import json
import random

numberOfNodes = 13
width = 800
height = 800
inputDir = "/Users/ronaklakhwani/Desktop/comparision/sampleData/data/"
outputDir = "/Users/ronaklakhwani/Desktop/comparision/clusteringData/data/"
fileName = "data_800.json"
finalClusters = []
nodeSet = []
nodeSetId = 800
nodesDict = {}
inputFileName = "/Users/ronaklakhwani/Desktop/comparision/sampleData/data/data_800.json"

#-- linksDict = {1: [2,3,4,5,6], 2: [1,3,4,5,6], 3: [1,2,4,5,6], 4: [1,2,3,5,6],
         # 5: [1,2,3,4,7,8], 6: [1,2,3,4,7,8], 7: [5,6,9,10,11,12,13], 8: [5,6,9,10,11,12,13],
         # 9: [7,8,10,11,12,13], 10: [7,8,9,11,12,13], 11: [7,8,9,10,12,13], 12: [7,8,9,10,11,13],
         #------------------------------------------------ 13: [7,8,9,10,11,12]}
         
linksDict = {1: [2,3,4,5,6], 2: [3,4,5,6], 3: [4,5,6], 4: [5,6],
         5: [7,8], 6: [7,8], 7: [], 8: [],
         9: [7,8,10,11,12,13], 10: [7,8,11,12,13], 11: [7,8,12,13], 12: [7,8,13],
         13: [7,8]}

def generateData(numberOfNodes,linksDict, width, height, fileName) :
    nodes = []
    links = []
    
    for i in range(1, numberOfNodes + 1) :
        node = {}
        node['id'] = i
        node['x'] = random.randrange(0,width)
        node['y'] = random.randrange(0,height)
        nodes.append(node)
        
    for source,targets in linksDict.items():
        for target in targets : 
            link = {}
            link['source'] = source
            link['target'] = target
            links.append(link)
        
    f = open(fileName,"w+")
    fileData = {'nodes' : nodes, 'links' : links} 
    json.dump(fileData, f, True) 
        


def getSecondLargestEigenVector(adjacencyMatrix) :
    eigenValues,eigenVectors = linalg.eig(adjacencyMatrix)
    #a = map(round,eigenValues.tolist(),[5] * len(eigenValues.tolist()))
    realValues = []
    for i,imag in enumerate(eigenValues.imag) :
        if imag == 0 :
            realValues.append((i,eigenValues.real[i]))
    realValues.sort(key = lambda tup : tup[1])
    
    if len(realValues) > 1 :
        index = realValues[1][0]
    
    #a = eigenValues
    #b = []
    #for i in a:
    #    b.append(i)
    #a.sort()
    #index = b.index(a[1])                    
    #eigenVectors.transpose()[index]
        eigenVector =     eigenVectors.transpose()[index]
        return eigenVector
    else : 
        return None

def getClusters(nodes,links) :
    #nodeIds = []
    #for node in nodes:
    #    nodeIds.append(node['id'])
    #nodeIds = map(str,nodeIds)
    nodeIds = nodes
    size = len(nodeIds)
    
    adj = numpy.matrix(numpy.zeros((size,size)))
    degreeArray = numpy.zeros(size)

    for link in links:
        sIndex = nodeIds.index(link['source']['id'])
        tIndex = nodeIds.index(link['target']['id'])
        value = adj[sIndex].item(tIndex) - 1
        adj.itemset((sIndex,tIndex),value)
        value = adj[tIndex].item(sIndex) - 1
        adj.itemset((tIndex,sIndex),value)
        if sIndex == tIndex :
            degreeArray[tIndex] += 2
        else :
            degreeArray[tIndex] += 1
            
    lap = adj.copy()
        
    for i,degree in enumerate(degreeArray) :
        lap.itemset((i,i),degree - lap[i].item(i))
        
    eigenVector = getSecondLargestEigenVector(lap)
    eigenVector = eigenVector.real
    if eigenVector != None :
        cluster1 = []
        cluster2 = []
        for i in range(eigenVector.shape[1]):
            s = eigenVector[0].item(i)
            if s >= 0 :
                cluster1.append(nodeIds[i])
            else :
                cluster2.append(nodeIds[i])
                
        #clusters = {}
        #clusters['cluster1'] = cluster1
        #clusters['cluster12'] = cluster2
        #clusters['adj'] = adj
        #clusters['nodeIds'] = nodeIds
        if len(cluster1) != 0 and len(cluster2) != 0 :
            clusters = []
            clusters.append(cluster1);
            clusters.append(cluster2);
            clusters.append("OK")
        else :
            clusters = []
            clusters.append(cluster1 if len(cluster1) != 0 else cluster2);
            clusters.append("DONE")
    else :
        clusters = []
        clusters.append(nodes)
        clusters.append("ERROR")
        
    return clusters       

def graphClustering(nodes,links,nodeSetIdInfo) :
    global nodeSetId 
    if len(nodes) >= 5 :
        clusters = getClusters(nodes, links);
        result = clusters.pop()
        if result == "OK" :
            for cluster in clusters :
                clusterLinks = [i for i in links if i['source']['id'] in cluster and i['target']['id'] in cluster]
                dummyNodeSetIdInfo = [] 
                graphClustering(cluster, clusterLinks, dummyNodeSetIdInfo)
                if len(dummyNodeSetIdInfo) > 1 :
                    aDict = {}
                    aDict['id'] = nodeSetId + 1
                    nodeSetId = nodeSetId + 1
                    aDict['type'] = 'nodeSet'
                    aDict['nodes'] = dummyNodeSetIdInfo
                    aDict['x'] = random.randrange(0,width)
                    aDict['y'] = random.randrange(0,height)
                    nodeSet.append(aDict)
                    nodeSetIdInfo.append(nodeSetId)
                elif len(dummyNodeSetIdInfo) == 1 :
                    nodeSetIdInfo.append(dummyNodeSetIdInfo[0])
        else :
            aDict = {}
            aDict['id'] = nodeSetId + 1
            nodeSetId = nodeSetId + 1
            aDict['type'] = 'nodeSet'
            aDict['nodes'] = nodes
            aDict['x'] = random.randrange(0,width)
            aDict['y'] = random.randrange(0,height)
            nodeSet.append(aDict) 
            finalClusters.append(clusters.pop())
            nodeSetIdInfo.append(nodeSetId)
    else : 
        if len(nodes) > 1 :
            aDict = {}
            aDict['id'] = nodeSetId + 1
            nodeSetId = nodeSetId + 1
            aDict['type'] = 'nodeSet'
            aDict['nodes'] = nodes
            aDict['x'] = random.randrange(0,width)
            aDict['y'] = random.randrange(0,height)
            nodeSet.append(aDict)
            nodeSetIdInfo.append(nodeSetId)
            finalClusters.append(nodes)
        else :
            nodeSetIdInfo.append(nodes[0])
            




if __name__ == '__main__' :
    
    #generateData(numberOfNodes, linksDict, width, height, inputDir + fileName)
    
    with open(inputFileName) as f:
        catalog = json.load(f)
        
    nodes = catalog['nodes']  
    links = catalog['links']  
    nodeIds = []
    
    for node in nodes:
        nodeIds.append(node['id'])
        nodesDict[node['id']] = node
    #nodeIds = map(str,nodeIds)
    nodeSetIdInfo = []
    
    graphClustering(nodeIds,links, nodeSetIdInfo)
    
    #print finalClusters
    print len(finalClusters)
    
    dictNodes = {}
    for node in nodes : 
        dictNodes[node['id']] = node
    #===========================================================================
    global nodeSetId
    nodeSet = []
    for cluster in finalClusters :
        aDict = {}
        aDict['id'] = nodeSetId + 1
        aDict['type'] = 'nodeSet'
        aDict['nodes'] = cluster
        aDict['x'] = random.randrange(0,width)
        aDict['y'] = random.randrange(0,height)
        aDict['x'] = dictNodes[cluster[0]]['x']
        aDict['y'] = dictNodes[cluster[0]]['y']
        print len(cluster)
        nodeSet.append(aDict)
        nodeSetId = nodeSetId + 1
    print nodeSet
    #===========================================================================
    f = open(outputDir + fileName,"w+")
    fileData = {'nodes' : nodes, 'links' : links, 'nodeSet': nodeSet} 
    json.dump(fileData, f, True) 
       