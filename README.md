# Amazon Crawler

Crawling and saving specific information from product page on `amazon.de`.

Workflow

1. Reading ASIN from MySQL.
2. Crawling on product page for each ASIN.
3. Store the information to MySQL.

## Prerequisites

Following are installed on local machine.

- Chrome
- ChromeDriver

On MacOS, ChromeDriver can be installed using Homebrew.

Note: project tested on ChromeDriver `79.0.3945.36` and Chrome `79.0.3945.88`.
