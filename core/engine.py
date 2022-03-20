import requests


class ContentDownloader:
    def __init__(self, uri):
        self._content_uri = uri
        self._is_graphql = True
        try:
            self._metadata = self._fetch_metadata()
        except Exception as e:
            raise Exception("Could not fetch metadata.") from e

    def get_media_type(self):
        if self._is_graphql:
            mtype = self._elem.get('__typename', None)
            return 'video' if mtype == 'GraphVideo' else 'image' if mtype == 'GraphImage' else 'unknown'

        mtype = self._elem.get('media_type', None)
        return 'video' if mtype == 2 else 'image' if mtype == 1 else 'unknown'

    def get_media_download_link(self):
        lnk = None
        if self.get_media_type() == 'video':
            if self._is_graphql:
                lnk = self._elem.get('video_url', None)
            else:
                v = self._elem.get('video_versions', [])
                if len(v) > 0:
                    lnk = v[0].get('url', None)
        elif self.get_media_type() == 'image':
            if self._is_graphql:
                lnk = self._elem.get('display_url', None)
            else:
                i = self._elem.get('image_versions', {}).get('candidates', [])
                if len(i) > 0:
                    lnk = i[0].get('url', None)
        else:
            return None

        return f"{lnk}&dl=1"

    def get_preview_link(self):
        if self.get_media_type() == 'image' or self.get_media_type() == 'video':
            if self._is_graphql:
                return self._elem.get('display_url', None)
            else:
                i = self._elem.get('image_versions', {}).get('candidates', [])
                if len(i) > 0:
                    return i[0].get('url', None)

        return None

    def _fetch_metadata(self):
        headers = {'content-type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0'}
        res = requests.get(f"{self._content_uri}?__a=1", headers=headers)
        data = res.json()
        if data.get('graphql', None) is None:
            self._is_graphql = False
        else:
            self._is_graphql = True
        print(data)
        return data

    @property
    def _elem(self):
        entry = {}
        if self._is_graphql:
            entry = self._metadata.get(
                'graphql', {}).get('shortcode_media', {})
        else:
            entries = self._metadata.get('items', [])
            if len(entries) > 0:
                entry = entries[0]
        return entry
