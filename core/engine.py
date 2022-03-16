import requests


class ContentDownloader:
    def __init__(self, uri):
        self._content_uri = uri
        try:
            self._metadata = self._fetch_metadata()
        except Exception as e:
            raise Exception("Could not fetch metadata.") from e

    def get_media_type(self):
        mtype = self._elem.get('__typename')
        return 'video' if mtype == 'GraphVideo' else 'image' if mtype == 'GraphImage' else 'unknown'

    def get_media_download_link(self):
        lnk = None
        if self.get_media_type() == 'video':
            lnk = self._elem.get('video_url', None)
        elif self.get_media_type() == 'image':
            lnk = self._elem.get('display_url', None)
        else:
            return None

        return f"{lnk}&dl=1"

    def get_preview_link(self):
        if self.get_media_type() == 'image' or self.get_media_type() == 'video':
            return self._elem.get('display_url', None)
        else:
            return None

    def _fetch_metadata(self):
        headers = {'content-type': 'application/json'}
        res = requests.get(f"{self._content_uri}?__a=1", headers=headers)
        data = res.json()
        print(data)
        return data

    @property
    def _elem(self):
        entry = self._metadata.get('graphql', {}).get('shortcode_media', {})
        return entry
