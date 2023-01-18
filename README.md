# VersionDB

I wanted to have an place where I can store versions of libraries and/or applications in a single place, without storing the actual binaries. The possibility to generate a sBOM (Software Bill of Materials) based on the artifacts that are part of a group or a category. A place that helps to determine the next available version that can be used for the artifact as part of a CI/CD pipeline.

VersionDB helps to achieve this. A place where artifacts can be configured, where versions can be created and a sBOM can be created. Also it allows to create a version of the sBOM, so that changes between sBOM versions can be tracked.

## How does it work


Post the following to `http://$URL:5001/api/v1/artifacts/`
```json
{
    "name": "myartifact",
    "category": "mycategory",
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

