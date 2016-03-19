#coding=utf-8
import sys,getopt,urllib,re,os,urlparse,datetime,urllib2,time
def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getImgcssjs(html,output_dir):
    print "start"
    timedir=datetime.datetime.now().strftime("%Y%m%d%H%M")
    updir=output_dir+'\\'+timedir
    os.mkdir(updir)

    css = r'<link rel="stylesheet" type="text/css" href="(.+?\.css)"'
    cssre = re.compile(css)
    csslist = cssre.findall(html)
    cssdir=updir+'\\'+'css'
    os.mkdir(cssdir)
    for cssurl in csslist:
        filename = cssurl.split("/")[-1]
        outpath = os.path.join(cssdir, filename)
        urllib.urlretrieve(cssurl,outpath)   
    """抓取并保存css文件"""

    img = r'<img src="(.+?\.jpg)" alt='
    imgre = re.compile(img)
    imglist = imgre.findall(html)
    imgdir=updir+'\\'+'images'
    os.mkdir(imgdir)
    for imgurl in imglist:
        filename = imgurl.split("/")[-1]
        outpath = os.path.join(imgdir,filename)
        urllib.urlretrieve(imgurl,outpath)    
        """抓取七张大图图片并保存""" 

    img = r'original="(.+?\.jpg)"'
    imgre = re.compile(img)
    imglist = imgre.findall(html)
    for imgurl in imglist:
        filename = imgurl.split("/")[-1]
        outpath = os.path.join(imgdir,filename)
        urllib.urlretrieve(imgurl,outpath)
    """抓取各分栏的图片"""
    

    js = r'<script type="text/javascript" src="(.+?\.js)">'
    jsre = re.compile(js)
    jslist = jsre.findall(html)
    jsdir=updir+'\\'+'js'
    os.mkdir(jsdir)
    for imgurl in jslist:
        filename = imgurl.split("/")[-1]
        outpath = os.path.join(jsdir, filename)
        urllib.urlretrieve(imgurl,outpath)     
    """爬取js文件并保存"""

    domain = urlparse.urlsplit(url)[1].split(':')[0].split('.')[1] 
    path = updir+'\\'+'index.html'
    os.mkdir(path)
    filename = domain+'.html'
    savefilepath = os.path.join(path,filename)
    req = urllib2.Request(url) 
    con = urllib2.urlopen( req )
    msg = con.read()
    original = r'<i class="img"><img src="(.+?\.jpg)" original="(.+?\.jpg)"'
    originalre =re.compile(original)
    originallist = originalre.findall(msg)
    for x in originallist:
        filename = x[1].split("/")[-1]
        imgdir=updir+'\\'+'images'+'\\'+filename
        msg = msg.replace(x[0],imgdir)
    file_object = open(savefilepath,'wb')
    file_object.write(msg)
    file_object.close()
    print "end"
    """爬取网页并保存"""
        

def main(average_time, url,output_dir):
    while 1:
        average_time=float(average_time)
        time.sleep(average_time)
        html = getHtml(url)
        getImgcssjs(html,output_dir)
if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "d:u:o:")
    average_time=1
    url=""
    output_file=""
    for op, value in opts:
        if op == "-d":
            average_time = value
        elif op == "-u":
            url = value
        elif op == "-o":
            output_dir = value
    main(average_time,url,output_dir)
