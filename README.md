# track-bulk-uploader

This tool helps uploading a large catalogue of tracks to the musiio search dashboard 
https://search.musiio.com. The data needs be in a tab-separated values(TSV) file. A sample can be found
here https://storage.googleapis.com/customer-public-us/documentation/sample_input.tsv. The reference for columns supported
can be found here https://docs.musiio.com/search/#/catalog/post_catalog_batch_add_tracks.


## Prerequisites
* Python 3.6+
* API Key to access the search api. Please email sales@musiio.com to obtain an API Key.

## Installation
```shell
git clone https://github.com/Musiio-AI/track-bulk-uploader.git
cd track-bulk-uploader
pip install -r requirements.txt
```

## Sample Usage
```shell
python -m track_bulk_uploader
Enter your API Key: <API-KEY>
Enter the path to the TSV: catalogue.tsv
Fetching Custom Fields...
Fetched Custom Fields
Validating TSV...
Successfully validated TSV
Uploading TSV...
Succesfully uploaded TSV. The tracks will take upto 24 hours to appear on the search dashboard https://search.musiio.com.
```

**_NOTE:_** If the number of tracks is greater than 100,000, please split the file into chunks of 100,000.