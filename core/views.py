from django.shortcuts import render
from django.views import View
from core.engine import ContentDownloader

from core.forms import ContentURLForm


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
            return render(request, 'download_page.html', context=ctx)
