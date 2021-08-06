class TSVOrchestrator:
    def __init__(self, tsv_path, tsv_validator, api_service):
        self.__tsv_validator = tsv_validator
        self.__api_service = api_service
        self.__tsv_path = tsv_path

    def fetch_custom_fields(self):
        error, response = self.__api_service.get_custom_fields()

        if error is None:
            custom_fields = {}
            custom_field_properties = response['properties']
            for property in custom_field_properties:
                property_id = property["id"]
                property_type = property["type"]
                custom_field = {
                    "required": False,
                    "internal_id": property_id,
                    "type": property_type
                }

                custom_fields[property_id] = custom_field

            return None, custom_fields
        elif error == 401:
            return "Please check the api key and try again.", None
        else:
            return "There was a connection error. Please try again in a few minutes.", None

    def validate_tsv(self, custom_fields, max_errors):
        return self.__tsv_validator.process_tsv(tsv_file_path=self.__tsv_path, custom_fields=custom_fields,
                                                max_errors=max_errors)

    def upload_tsv(self):
        error, response = self.__api_service.upload_tsv(self.__tsv_path)
        if error is None:
            return None
        elif error == 401:
            return "Please check the api key and try again."
        else:
            return "There was a connection error. Please try again in a few minutes."
