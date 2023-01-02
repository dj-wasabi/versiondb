# VersionDB


VersionDB is 


## How does it work


Post the following to `http://$URL:5001/api/v1/artifact/`
```json
{
    "name": "myartifact",
    "group": "mygroup",
    "url": "https://some.docs.url/myartifat.hml",
    "git": "git://some.git.url/myartifact.git",
    "version": "0.1.1",
    "metadata": [
        {
            "key": "MY_IMPORTANT_KEY",
            "value": "SOME_VALUE"
        }
    ]
}
```

