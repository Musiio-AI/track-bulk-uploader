from track_bulk_uploader.tsv_orchestrator import TSVOrchestrator
from musiio_validate_tsv.validate_tsv import ValidateTSV
from track_bulk_uploader.services import APIService
import os
import json


class InputManager:
    @staticmethod
    def run_track_bulk_uploader():
        api_key = input("Enter your API Key: ")
        tsv_path = input("Enter the path to the TSV: ")

        if not os.path.exists(tsv_path):
            print("Invalid TSV path provided.")
            return

        try:
            max_errors = int(os.getenv("MAX_ERRORS", 10))
            if max_errors <= 0:
                print("MAX_ERRORS has to be greater than zero.")
                return
        except:
            print("Invalid value for max errors. It has to be an integer.")
            return

        tsv_validator = ValidateTSV()
        api_service = APIService(api_key=api_key)
        tsv_orchestrator = TSVOrchestrator(tsv_path=tsv_path, tsv_validator=tsv_validator, api_service=api_service)

        print("Fetching Custom Fields...")
        error, custom_fields = tsv_orchestrator.fetch_custom_fields()
        if error:
            print("Could not fetch Custom Fields. {}".format(error))
            return
        print("Fetched Custom Fields")

        print("Validating TSV...")
        errors, _ = tsv_orchestrator.validate_tsv(custom_fields=custom_fields, max_errors=max_errors)
        if errors:
            print("Error validating TSV.")
            print("{}".format(json.dumps(errors, indent=4,)))
            return
        print("Successfully validated TSV")

        print("Uploading TSV...")
        error = tsv_orchestrator.upload_tsv()
        if error:
            print("Could not upload TSV. {}".format(error))
            return
        print("Succesfully uploaded TSV. "
              "The tracks will take upto 24 hours to appear on the search dashboard https://search.musiio.com.")


