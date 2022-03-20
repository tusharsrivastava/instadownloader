from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from core.engine import ContentDownloader

from core.forms import ContentURLForm


@method_decorator(csrf_exempt, name='dispatch')
class Index(View):
    def get(self, request):
        form = ContentURLForm()
        ctx = {
            'form': form,
        }
        return render(request, 'index.html', context=ctx)

    def post(self, request):
        form = ContentURLForm(request.POST)
        if not form.is_valid():
            ctx = {
                'form': form,
            }
            return render(request, 'index.html', context=ctx)
        else:
            downloader = ContentDownloader(form.cleaned_data['content_url'])
            ctx = {
                'preview_link': downloader.get_preview_link(),
                'download_link': downloader.get_media_download_link(),
                'media_type': downloader.get_media_type(),
            }
            format = request.GET.get("format", "")
            if format.lower() == "json":
                return JsonResponse(ctx)
            return render(request, 'download_page.html', context=ctx)
