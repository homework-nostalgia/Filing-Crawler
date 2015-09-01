import urllib2
import os
 
 
def crawl(url):
      global filings
      html = urllib2.urlopen(url)
      data = html.read().replace('\n','').replace('\t','').replace('  ','')
      idlist = []
      namelist = []
      index = 0
      while(data.find("""onclick="window.location='filings-case.html?id=""")>0):
            index = data.find("""onclick="window.location='filings-case.html?id=""")+47
            idlist.append(data[index:index+6])
            nameend = data.find('</td>',index)
            namelist.append(data[index+22:nameend])
            data = data[index:]
      forbiddencharlist = ['<','>',':','"','/','\\','|','?','*']
      i=0
      for item in namelist:
            for char in forbiddencharlist:
                  namelist[i] = namelist[i].replace(char,'')
            i+=1
      os.chdir("/textdocs")
      filings+=len(idlist)
      write(idlist,namelist)
     
def write(idllist,namelist):
      i=0
      os.chdir("/textdocs")
      for item in idllist:
            data = urllib2.urlopen("http://securities.stanford.edu/filings-case.html?id="+item).read()
            with open(namelist[i]+'.txt','w+') as f:
                  f.write(data)
            i+=1
     
           
def getlastpage():
      page = 500
      print "Preparing search...."
      pagerange = [7,65500]
      while(pagerange[1]-pagerange[0]!=1):   
            url = "http://securities.stanford.edu/filings.html?page="+str(page)
            data = urllib2.urlopen(url).read()            
            if (data.find("?page=6.0")<0):
                  pagerange[0] = page
                  page = page+max((pagerange[1]-pagerange[0])/2,1)
            else:
                  pagerange[1] = page
                  page = page-max((pagerange[1]-pagerange[0])/2,1)
      return pagerange[0]
            
    
      
if not os.path.exists("/textdocs"):
      os.makedirs("/textdocs")
global filings
filings=0
connectioncheck = False
try:  
      print "Attempting to establish connection with server..."
      urllib2.urlopen("http://securities.stanford.edu/filings.html")
      connectioncheck = True
      print "Connection successful"
           
except:
      print "unable to communcate with server."
      
totalpages = getlastpage()
for page in range(1,totalpages+1):
      url = "http://securities.stanford.edu/filings.html?page="+str(page)
      crawl(url)
      print ('%.2f'%(float(filings*100)/(totalpages*20))+"% complete...") 
