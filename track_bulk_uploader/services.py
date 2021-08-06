import requests
from requests.auth import HTTPBasicAuth


class APIService:
    BASE_URL = "https://api-us.musiio.com/v2"

    def __init__(self, api_key):
        self.__api_key = api_key
        self.__auth = HTTPBasicAuth(api_key,'')

    def get_custom_fields(self):
        try:
            response = requests.get('{}/search/mapping'.format(APIService.BASE_URL), auth=self.__auth, timeout=10)
        except Exception:
            return 500, None

        if response.status_code == 200:
            json_response = response.json()
            return None, json_response
        else:
            return response.status_code, None

    def upload_tsv(self, tsv_path):
        tsv_file = open(tsv_path, 'rb')
        files = {'file': tsv_file}
        try:
            response = requests.post('{}/catalog/batch-add-tracks'.format(APIService.BASE_URL), files=files, auth=self.__auth,
                                     timeout=300)
        except Exception:
            tsv_file.close()
            return 500, None

        tsv_file.close()
        if response.status_code == 200:
            json_response = response.json()
            return None, json_response
        else:
            return response.status_code, None
