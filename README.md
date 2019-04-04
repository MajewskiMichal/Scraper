Scraper
========


REST application for parsing webpage and scraping text and images from it.


# Running

When you are in docker-compose.yml directory, this repo can be run by typing:

``` bash
$ docker-compose up
```

### Scrape text

**Definition**

`POST /api/persist_text`

**Response**

- `"success": "Text parsed into /tmp{webpage name}.txt` on success

```json
    {
        "url": "https://en.wikipedia.org/wiki/Python"

    }
```

### Scrape images

**Definition**

`POST '/api/persist_image`

**Response**

- `"success": "success": "Images parsed into tmp catalogue"` on success

```json
    {
        "url": "https://en.wikipedia.org/wiki/Python"

    }
```

### To be implemented:
threading,
db,
unitests

