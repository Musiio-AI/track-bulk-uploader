import responses
import unittest
from track_bulk_uploader.services import APIService


class TestValidateTSV(unittest.TestCase):
    @responses.activate
    def test_get_custom_fields(self):
        # Returns status code of api if error with None response
        responses.add(responses.GET, APIService.BASE_URL + "/search/mapping", status=500)
        responses.add(responses.GET, APIService.BASE_URL + "/search/mapping", body=Exception())
        responses.add(responses.GET, APIService.BASE_URL + "/search/mapping", json={
            "hello": "world"
        }, status=200)

        api_service = APIService(api_key="fake_key")
        error, response = api_service.get_custom_fields()
        self.assertIsNone(response)
        self.assertEqual(error, 500)

        # Returns 500 as status code if exception with None response

        error, response = api_service.get_custom_fields()
        self.assertIsNone(response)
        self.assertEqual(error, 500)

        # Returns response json if status code is 200 with error set to None
        api_service = APIService(api_key="fake_key")
        error, response = api_service.get_custom_fields()
        self.assertIsNone(error)
        self.assertEqual(response, {
            "hello": "world"
        })

    @responses.activate
    def test_upload_tsv(self):
        # Returns status code of api if error with None response
        responses.add(responses.POST, APIService.BASE_URL + "/catalog/batch-add-tracks", status=500)
        responses.add(responses.POST, APIService.BASE_URL + "/catalog/batch-add-tracks", body=Exception())
        responses.add(responses.POST, APIService.BASE_URL + "/catalog/batch-add-tracks", json={
            "hello": "world"
        }, status=200)

        api_service = APIService(api_key="fake_key")
        error, response = api_service.upload_tsv(tsv_path="tests/tsv_files/valid_all_fields.tsv")
        self.assertIsNone(response)
        self.assertEqual(error, 500)

        # Returns 500 as status code if exception with None response

        error, response = api_service.upload_tsv(tsv_path="tests/tsv_files/valid_all_fields.tsv")
        self.assertIsNone(response)
        self.assertEqual(error, 500)

        # Returns response json if status code is 200 with error set to None
        api_service = APIService(api_key="fake_key")
        error, response = api_service.upload_tsv(tsv_path="tests/tsv_files/valid_all_fields.tsv")
        self.assertIsNone(error)
        self.assertEqual(response, {
            "hello": "world"
        })