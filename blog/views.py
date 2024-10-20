from django.views.generic import TemplateView
from django.shortcuts import render

class IndexView(TemplateView):
    template_name = 'index.html'

# Es importante que el argumento exception esté presente
# para que Django lo pueda identificar como un manejador de errores
def not_found_view(request, exception):
    return render(request, 'errors/error_not_found.html', status=404)

def internal_error_view(request):
    return render(request, 'errors/error_internal.html', status=500)

def forbidden_view(request, exception):
    return render(request, 'errors/error_forbidden.html', status=403)