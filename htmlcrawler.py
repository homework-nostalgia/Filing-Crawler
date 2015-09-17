import urllib2
import os
import sys
 
 
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
      filings+=len(idlist)
      for item in idlist:
            write(scrub_page("http://securities.stanford.edu/filings-case.html?id="+item))
     
def write(newcsvline):
      with open(os.getcwd().replace("\\",'/')+'/csvoutput/csvdata.csv','a') as f:
            f.write(newcsvline+"\n")
            f.close()
     
           
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
 
 
 
def scrub_page(url):
      data = urllib2.urlopen(url).read()
      casestatus = get_case_status(data)
      casedate = get_case_date(data)
      defendant = get_defendant(data)
      sector = get_sector(data)
      industry = get_industry(data)
      hq = get_hq(data)
      ticker = get_ticker(data)
      comarket = get_company_market(data)
      marketstatus = get_market_status(data)
     
      marker = data.find('<h3>Reference Complaint</h3>')
      if (marker>=0):
            data = data[marker:]  
           
      court = get_court(data)
      docket = get_docket(data)
      judge = get_judge(data)
      filedate = get_filedate(data)
      periodstart = get_period_start(data)
      periodend = get_period_end(data)
      complaintinfo = getcomplaintinfo(data)
      complaintdate = complaintinfo[0]
      pdfdata = complaintinfo[1]
      writepdf(complaintpdf)
      csvrow = (casestatus+"!@#$%^"+casedate+"!@#$%^"+defendant+"!@#$%^"+sector+"!@#$%^"+industry+"!@#$%^"+hq+"!@#$%^"+ticker+"!@#$%^"+comarket+"!@#$%^"+marketstatus+"!@#$%^"+court+"!@#$%^"+docket+"!@#$%^"+judge+"!@#$%^"+filedate+"!@#$%^"+periodstart+"!@#$%^"+periodend).replace(',','').replace('!@#$%^',',')
      return csvrow
     
 
def get_case_status(data):
      marker = data.find('<strong>Case Status: &nbsp;&nbsp;</strong>')
      data = data[marker:]
      markend = 0
      i=0  
      n=0
      while(n<3):
            if (data[i] == '\n'):
                  markend=i
                  n+=1
            i+=1
      data = data[0:markend]
      casestatus = ""
      if (data.find('ONGOING')>0):
            casestatus = 'ONGOING'
      elif (data.find('DISMISSED')>0):
            casestatus = 'DISMISSED'
      elif (data.find('SETTLED')>0):
            casestatus = 'SETTLED'
      return casestatus
 
def get_case_date(data):
      marker = data.find('On or around ')+13
      casedate = data[marker:marker+10]  
      return casedate
 
def get_defendant(data):
      data = data[data.find('Defendant: '):]
      data = data[11:data.find('\n')]
      defendant = data.replace(' <small> <a href="">website</a> </small></h4>','')
      return defendant
 
def get_sector(data):
      data = data[data.find('Sector:'):]
      data = data[16:data.find('\n')]
      sector = data.replace('</div>','')
      return sector
 
def get_industry(data):
      data = data[data.find('Industry:'):]
      data = data[19:data.find('\n')]
      industry = data.replace('</div>','')
      return industry
 
def get_hq(data):
      data = data[data.find('Headquarters:'):]
      data = data[23:data.find('\n')]
      hq = data.replace('</div>','')
      return hq
 
def get_ticker(data):
      data = data[data.find('Ticker Symbol:'):]
      data = data[24:data.find('\n')]
      ticker = data.replace('</div>','')
      return ticker
 
def get_company_market(data):
      data = data[data.find('Company Market:'):]
      data = data[25:data.find('\n')]
      comarket = data.replace('</div>','')
      return comarket
     
def get_market_status(data):
      data = data[data.find('Market Status:'):]
      data = data[24:data.find('\n')]
      marketstatus = data.replace('</div>','')
      return marketstatus
 
#the following are the ones in question
 
def get_court(data):
      data = data[data.find('COURT:'):]
      data = data[16:data.find('\n')]
      court = data.replace('</div>','')
      return court
 
def get_docket(data):
      data = data[data.find('DOCKET #:'):]
      data = data[19:data.find('\n')]
      docket = data.replace('</div>','')
      return docket
 
def get_judge(data):
      data = data[data.find('JUDGE:'):]
      data = data[16:data.find('\n')]
      judge = data.replace('</div>','')
      return judge
 
def get_filedate(data):
      data = data[data.find('DATE FILED:'):]
      data = data[21:data.find('\n')]
      filedate = data.replace('</div>','')
      return filedate
 
def get_period_start(data):
      data = data[data.find('CLASS PERIOD START:'):]
      data = data[29:data.find('\n')]
      periodstart = data.replace('</div>','')
      return periodstart
 
def get_period_end(data):
      data = data[data.find('CLASS PERIOD END:'):]
      data = data[27:data.find('\n')]
      periodend = data.replace('</div>','')
      return periodend
 
def getcomplaintinfo(data):
      docdata = []
      rows = []
       
      while(data.find("""<tr class="table-link" onclick="window.location='""")>=0):
            data = data[data.find("""<tr class="table-link" onclick="window.location='""")+49:]
            nth = data.find('\n')
            n=4
            while((nth>=0)and(n>1)):
                  nth = data.find('\n', nth+1)
                  n -= 1
            end = nth
            rowdata = data[:end]
            rows.append(rowdata.split('\n'))
            data = data[end:]
          
      
      #THIS IS WHERE I LEFT OFF. INCLUDE THET NAME, SO THAT THE PDFWRITER CAN NAME THE FILE.
      for item in rows:
            if ('complaint' in item[2][item[2].find('<td>')+4:item[2].find('</td>')].lower()):
                  docdata.append([item[0][:item[0].find('.pdf')+4],item[3][item[3].find('<td>')+4:item[3].find('</td>')]])
      n=-1
      maxyear = 0
      maxmon = 0
      maxday = 0
      for item in docdata:
            datesplit = item[1].split('/')
            if (int(datesplit[2])>maxyear):
                  maxyear = int(datesplit[2])
                  maxmon = int(datesplit[0])
                  maxday = int(datesplit[1])
                  n+=1
            elif ((int(datesplit[2])==maxyear)and(int(datesplit[0])>maxmon)):
                  maxmon = int(datesplit[0])
                  maxday = int(datesplit[1])
                  n+=1
            elif (((int(datesplit[2])==maxyear)and(int(datesplit[0])>maxmon))and(int(datesplit[1])>maxday)):
                  maxday = int(datesplit[1])
                  n+=1
          
      address = "http://securities.stanford.edu/"+docdata[n][0]
      
      pdfdata = urllib2.openurl(address).read()
      date = str(maxmon)+"/"+str(maxday)+"/"+str(maxyear)
      return (date,pdfdata)

#def writepdf(pdfdata):
      #with open(
     
 
 

           
csvanswer = raw_input('data will be written to '+str(os.getcwd())+"\\csvoutput\\csvdata.csv, is this okay? (y/n): ")
if ((csvanswer.lower() != "y")and(csvanswer.lower() != "yes")):
      sys.exit(0)
      
pdfpdfanswer = raw_input('complaint pdfs will be written in '+str(os.getcwd())+"\\complaintdocs\\, is this okay? (y/n): ")
if ((pdfanswer.lower() != "y")and(pdfanswer.lower() != "yes")):
      sys.exit(0)
     
if not os.path.exists(os.getcwd().replace("\\",'/')+"/csvoutput/"):
      os.makedirs(os.getcwd().replace("\\",'/')+"/csvoutput")
if not os.path.isfile("/csvoutput/csvdata.csv"):
      with open(os.getcwd().replace("\\",'/')+'/csvoutput/csvdata.csv','w+') as f:
            f.write("")
            f.close()    
if not os.path.exists(os.getcwd().replace("\\",'/')+"/complaintdocs/"):
      os.makedirs(os.getcwd().replace("\\",'/')+"/complaintdocs")
      
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
      html = urllib2.urlopen(url)
      data = html.read()
      crawl(url)
      print ('%.2f'%(float(filings*100)/(totalpages*20))+"% complete...")
