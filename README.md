# citadextract
This is a private moodle scraping API written using Flask and BS4

### Basic
Just replace the contents of the config.json file with your own moodle courses. For example, go to individual course and news forum pages and note down the `id` key at the end of the URL.

#### Why did I do this?
Because 5min of manual work can save hours of automation. Also, fetching these course links dynamically would end up expending more resources and time at the API server.
