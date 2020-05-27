from django.shortcuts import render, HttpResponse
import sys
sys.path.append('..')
from indexbuilder.query import Query

q = Query('../indexbuilder/index')

def search_form(request):
    return render(request, 'main.html')

def search(request):
    res = None
    if 'q' in request.GET and request.GET['q']:
        res = q.standard_search(request.GET['q'])
        c = {
            'query': request.GET['q'],
            'resAmount': len(res),
            'results': res,
        }
    else:
        return render(request, 'main.html')

    # str = ''
    # for i in res:
    #     str += '<p><a href="' + i['newsUrl'] + '">' + i['newsTitle'] + '</a></p>'
    # return HttpResponse(str)

    return render(request, 'result.html', c)
