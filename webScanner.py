import os
import urllib.request
import io
from tld import get_tld


ROOTDIR = 'sites'

def gatherInfo(name, url):
    domainName = getDomainName(url)
    ipAddress = getIpAddress(url)
    nmap = getNmap('-F', ipAddress)
    robotsTxt = getRobotsTxt(url)
    whois = getWhoIs(domainName)
    createReport(name, url,domainName, nmap, robotsTxt, whois)

def createReport(name, url,domainName, nmap, robotsTxt, whois):
    projectDir = ROOTDIR + '/' + name
    createDir(projectDir)
    writeFile(projectDir + '/url.txt', url )
    writeFile(projectDir + '/domainName.txt', domainName)
    writeFile(projectDir + '/nmap.txt', nmap)
    writeFile(projectDir + '/robotsTxt.txt', robotsTxt)
    writeFile(projectDir + '/whois.txt', whois)

def createDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def writeFile(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()

def getIpAddress(url):
    command = "host " + url
    process = os.popen(command)
    result = str(process.read())
    mark = result.find('has address') + 12
    return result[mark:].splitlines()[0]

def getDomainName(url):
    domainName = get_tld(url)
    return domainName

def getNmap(options, ip):
    command = "nmap " + options + " " + ip
    process = os.popen(command)
    result = str(process.read())
    return result

def getRobotsTxt(url):
        if url.endswith('/'):
            path = url
        else:
            path = url + '/'
        req = urllib.request.urlopen(path + "robots.txt", data=None)
        data = io.TextIOWrapper(req, encoding='utf-8')
        return data.read()

def getWhoIs(url):
    command = "whois " + url
    process = os.popen(command)
    result = str(process.read())
    return result


createDir(ROOTDIR)