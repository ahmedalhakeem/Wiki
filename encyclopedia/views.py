import re
import random
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        
    })

def entry(request, title):
    #Get the entry content
    text= util.get_entry(title)
    #Check to see if text is there or not
    if text == None:
        message="The requseted page was not found"
        return render(request, "encyclopedia/error.html",{
            "message":message
        })
    #convert markdown links to HTML tag links
    p=re.compile(r'\[(.+?)\]\((.+?)\)')
    m=p.sub(r'<a href="\g<2>">\g<1></a>', text)
    #Convert Markdown heading
    def subsitute(m):
        return '<h{level}>{header}</h{level}>'.format(level=len(m.group(1)), header=m.group(2))
    def markdown_parser(markdown):
        results = [re.sub(r'(#{1,6}) (\w+)', subsitute, line) for line in markdown.split('\n')]
        return "\n".join(results).strip()
    m=markdown_parser(m)
    
    #Convert unordered list 
    p=re.compile(r'(^[*])\s+([\w]+\s?\w+)!?', re.MULTILINE)
    m=p.sub(r'<li>\g<2></li>', m)
    ulPattern = re.compile(r'<li>.+</li>', re.DOTALL)
    m = ulPattern.sub(r'<ul>\n\g<0>\n</ul>', m)

    #Convert text styling.
    p=re.compile(r'\*{2}(.+?)\*{2}', re.MULTILINE)
    m=p.sub(r'<b>\g<1></b>', m)

    #Convert Paragraph (open tag)
    p=re.compile(r'(^\w.*)(\.|\s)$', re.MULTILINE)
    m=p.sub(r'<p>\g<1></p>', m)
    
    #Convert Paragraph closed tag)
   # p=re.compile(r'(\.)$', re.MULTILINE)
   # m=p.sub(r'\g<1></p>', m)
    
    return render (request, "encyclopedia/entry.html", {
        "title" : title, 
        "content": m
        

    })
def results(request):
    entries = util.list_entries()
    if request.method=="POST":
        query = request.POST['q']
        result=[]
        #Loop through all items to find the match
        for item in entries:
            match=re.search(f".*{query}.*", item, re.IGNORECASE)
            if match != None:
                if match.group().upper() == query.upper():
                    return HttpResponseRedirect(reverse('entry', args=(query,)))
                   
                else:
                    result.append(item)
        
    return render(request, "encyclopedia/results.html",{
        "list": result
        
    })
    
def create(request):
    if request.method=="POST":
        title = request.POST['title']
        content = request.POST['content']
        
        if title == "" or content == "":
            return render ( request, "encyclopedia/error.html", {
                "message": "Either title or content is left blank!"
            }) 

        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "message": "The entry already exists"
            })
        
        else:
            new_entry = util.save_entry(title, content)
            return HttpResponseRedirect(reverse('entry', args=(title,)))
    else:
        return render(request, "encyclopedia/create_page.html")
    


def editpage(request, title):
    
    content= util.get_entry(title)
    
    if request.method=="POST":
        new_title=request.POST['newtitle']
        newcontent=request.POST['newcontent']
        if new_title == title:
            content = newcontent
            existentry=util.save_entry(title, content)
            return HttpResponseRedirect(reverse('entry', args=(title,)))
    

    return render(request, "encyclopedia/editpage.html",{
        "title": title,
        "content": content
    })

def random_entry(request):
    list_of_entries=util.list_entries()
    
    pickup=random.choice(list_of_entries)
    return HttpResponseRedirect(reverse('entry', args=(pickup,)))