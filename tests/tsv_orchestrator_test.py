import responses
import unittest
from unittest.mock import MagicMock

from track_bulk_uploader.tsv_orchestrator import TSVOrchestrator
from track_bulk_uploader.services import APIService
from musiio_validate_tsv.validate_tsv import ValidateTSV


class TestTSVOrchestrator(unittest.TestCase):
    def test_fetch_custom_fields(self):
        tsv_validator = ValidateTSV()
        api_service = APIService(api_key="fake_key")
        tsv_orchestrator = TSVOrchestrator(tsv_path="tests/tsv_files/valid_all_fields.tsv",
                                           tsv_validator=tsv_validator,
                                           api_service=api_service)
        # returns error if api returns error
        api_service.get_custom_fields = MagicMock(return_value=(400, None))
        error, custom_fields = tsv_orchestrator.fetch_custom_fields()
        self.assertIsNone(custom_fields)
        self.assertIsNotNone(error)

        # returns custom fields if no error from api
        api_service.get_custom_fields = MagicMock(return_value=(None, {
            "properties": [
                {
                    "id": "composer",
                    "type": "string",
                    "public": True
                },
                {
                    "id": "release_date",
                    "type": "date",
                    "public": False
                }
            ]
        }))

        error, custom_fields = tsv_orchestrator.fetch_custom_fields()
        self.assertIsNone(error)
        self.assertDictEqual(custom_fields, {
            "composer": {
                "required": False,
                "internal_id": "composer",
                "type": "string"
            },
            "release_date": {
                "required": False,
                "internal_id": "release_date",
                "type": "date"
            }
        })

    def test_validate_tsv(self):
        tsv_validator = ValidateTSV()
        api_service = APIService(api_key="fake_key")
        tsv_orchestrator = TSVOrchestrator(tsv_path="tests/tsv_files/valid_all_fields.tsv",
                                           tsv_validator=tsv_validator,
                                           api_service=api_service)

        # returns error if validator returns returns error
        tsv_validator.process_tsv = MagicMock(return_value=("error", None))
        error, processed_rows = tsv_orchestrator.validate_tsv(custom_fields={}, max_errors=5)
        self.assertIsNotNone(error)
        self.assertIsNone(processed_rows)

        # returns rows if validator succeeds
        tsv_validator.process_tsv = MagicMock(return_value=(None, {"data": "value"}))
        error, processed_rows = tsv_orchestrator.validate_tsv(custom_fields={}, max_errors=5)
        self.assertIsNone(error)
        self.assertDictEqual(processed_rows, {
            "data": "value"
        })

    def test_upload_tsv(self):
        tsv_validator = ValidateTSV()
        api_service = APIService(api_key="fake_key")
        tsv_orchestrator = TSVOrchestrator(tsv_path="tests/tsv_files/valid_all_fields.tsv",
                                           tsv_validator=tsv_validator,
                                           api_service=api_service)
        # returns error if error from api
        api_service.upload_tsv = MagicMock(return_value=(400, None))
        error = tsv_orchestrator.upload_tsv()
        self.assertIsNotNone(error)

        # returns None if no error from api
        api_service.upload_tsv = MagicMock(return_value=(None, None))

        error = tsv_orchestrator.upload_tsv()
        self.assertIsNone(error)
