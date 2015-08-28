## get RxNorm info from NIH using the restfull APIs and connection pooling
## this will build out rxnorm metadata, grown from classtree3.2.py

from urllib3 import HTTPConnectionPool
import json

def getJson(myRequest):
    r = http_pool.urlopen('GET', myRequest)
    return r.data

def getLastOfPath(path):
    return path.split('\\')[-1]    

def parseList(myList, c, hStr=None):
    # get the items in the list, it should have 1 (one) or more dict(s) named "rxclassMinConceptItem"
    # and 1 (one) list named "rxclassTree", except the last level(4) will not have the list
    # creates levels 1 - 5
    if hStr is None:
        hStr = '\\Meds\\'   
    
    for m in sorted(myList):
        if isinstance(m,dict):
            # get the items of the dict
            for k, v in sorted(m.iteritems()):
                if isinstance(v,dict):
                    classId = list(v.values())[0]
                    className = list(v.values())[1]
                    # when at the last time get json from 
                    # http://rxnav.nlm.nih.gov/REST/rxclass/classMembers?classId=J01EA&relaSource=ATC
                    # using classId
                    pathStr = hStr + classId
                    outStr = str(c) + '|' + pathStr + '\\|' + className + '|' + folder + '|ATC:' + classId
                    fileOut(outStr)
                    if c == 5:
                        getIngredients(pathStr,c+1)
                    
                elif isinstance(v,list):
                    # print '\tWe have a list for ' + classId #type(m)
                    hString = hStr + classId + '\\';  # print hString
                    parseList(v,c+1, hString)
                else:
                    print 'we never get here :('
        else:
            print 'MIKE!!!!'
    
def getIngredients(pathStr,c):
    # creates level 6
    cId = getLastOfPath(pathStr)
    # print cId
    
    url = '/REST/rxclass/classMembers.json?classId=' + cId + '&relaSource=ATC'
    # print url
    iResult = getJson(url)
    ingredient = json.loads(iResult)
    # print json.dumps(ingredient, sort_keys=True, indent=2)
    for k,v in ingredient.iteritems(): # go to drugMemberGroup level
        if k == 'drugMemberGroup':
            for k2,v2 in v.iteritems(): # go to drugMember level
                for me in v2: # enter into the list ingredients
                    for k3, v3 in me.iteritems(): # hold minConcept (dict and nodeAttr (list of dicts) objects
                        if k3 == 'minConcept':
                            name = list(v3.values())[1]
                            rxcui = list(v3.values())[2]
                            newPathStr = pathStr + '\\' + rxcui
                            outStr = str(c) + '|' + newPathStr + '\\|' + name + '|' + folder + '|RXNORM:' + rxcui ### last bit needs to be 'RXNORM:rxcui'
                            fileOut(outStr)
                            # go get prescribable drugs and their RXNORM codes 
                            getPrescribableDrugs(newPathStr,c+1)
                        
def getPrescribableDrugs(pathStr, c):
    # create level 7
    # print pathStr
    rxcui = getLastOfPath(pathStr)
    # get both the genric and branded drug from the ingredient rxcui 
    # using: http://rxnav.nlm.nih.gov/REST/rxcui/<generic rxcui>/related.json?tty=SCD+SBD'
    url = '/REST/rxcui/'+rxcui+'/related.json?tty=SBD+SCD+GPCK+BPCK'
    # print url
    pDResult = getJson(url)
    prescribable = json.loads(pDResult)
    relatedGroup = list(prescribable.values())[0]
    # print relatedGroup
    # loop through the json and get each sbd, scd, bpck and gpck
    for i in range(0,4):
        try:
            tty = list(relatedGroup.values())[0][i]['tty']
            gConceptPropertiesList = list(relatedGroup.values())[0][i]['conceptProperties']
            # print 'get gConceptPropertiesList'
            # print tty
        except KeyError: # we get a keyerror when there are is not a conceptProperties item, which can be normal.
            pass
            # print '************************************************************************'
            # print 'No ' + tty
            # print '************************************************************************'
        else:
            for gcp in gConceptPropertiesList:    
                for kgcp, vgcp in gcp.iteritems():
                    if kgcp == 'tty': tty = vgcp
                    elif kgcp == 'name': name = vgcp
                    elif kgcp == 'rxcui': rxcui = vgcp
                    # print kgcp
                # send this to the fileOut
                # print tty + ' name = ' + name + ' path = ' + pathStr + '\\' + rxcui +'\\'
                gPathStr = pathStr + '\\' + rxcui
                outStr = str(c) + '|' + gPathStr + '\\|' + name + '|' + folder + '|RXNORM:' + rxcui
                fileOut(outStr)
                print rxcui + ' passed to getNDC;'
                getNDC(gPathStr,c+1)
        
def getNDC(bPathStr, c):
    # creates level 8; get NDC for the branded drug or pack 
    # using: http://rxnav.nlm.nih.gov/REST/rxcui/<sbd rxcui>/ndcs.json
    rxcui = getLastOfPath(bPathStr)
    url = '/REST/rxcui/'+rxcui+'/allndcs.json'
    print url
    nDCResult = getJson(url)
    # # gNDC = json.loads(nDCResult)
    # # a = list(json.loads(nDCResult).values())[0]['ndcTime']['ndc']
    if list(json.loads(nDCResult).values())[0] is not None:
        # # print 'object is : ' + str(type(list(json.loads(nDCResult).values())[0]['ndcTime']))
        # # print list(json.loads(nDCResult).values())[0]['ndcTime']['ndc']
        for a in list(json.loads(nDCResult).values())[0]['ndcTime']:
            for kndc, vndc in a.iteritems():
                if kndc == 'ndc': ndcCode = vndc
            # mustbe str(ndcCode[0]) as what gets returned is [{"ndc":["00074010150"],"startDate":"200902","endDate":"201508"}]
            # the value of "ndc" is a list
            outStr = str(c) + '|' + bPathStr + '\\' +  str(ndcCode[0]) + '\\|' + str(ndcCode[0]) + '|' + leaf + '|NDC:' + str(ndcCode[0])
            # print outStr
            fileOut(outStr)

def fileOut(printStr):
    # accepts a string to print to the csv file
    
    pad =''
    for i in range(int(printStr.split('|')[0])): pad = pad + ' '

    print pad,    # comment out to turn off padding
    print printStr
    f.write(printStr + '\n')




outFilename = __file__.split('.')[0] + '.csv'

folder = 'FA'
leaf = 'LA'

# open our output file for writing
f = open(outFilename,'w')

hStr = '\\Med\\'
fileOut('0|'+ hStr + '|Medications|CA|ATC:Med')    

url = 'http://rxnav.nlm.nih.gov/REST/rxclass/classTree.json?classId=0'
# Create a connection pool for a specific host
http_pool = HTTPConnectionPool('rxnav.nlm.nih.gov')

# get the ATC heirarchy
request = '/REST/rxclass/classTree.json?classId=0'

classId = getJson(request)
parsed = json.loads(classId)
# print classId
    
for key, value in parsed.iteritems():
   if key == 'rxclassTree':
       parseList(value,1,hStr)
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       