# VersionDB

_Why?_

I needed a place to store versions of libraries or applications, without storing the actual artifacts. That place would allow me to add/update information in an automated way from the CI/CD pipeline. A central place containing all the artifacts to generate a sBOM based on a group or category. A sBOM that I then also could version as well.

VersionDB helps to achieve this. An API where you can an artifact, and as part of the CI/CD pipeline a version can stored. Once you have added a version, you can add/update information for extra validation like a commit or an hash. Any of these information sources can be used with the generation of the sBOM.

[![MasterRun](https://github.com/dj-wasabi/versiondb/actions/workflows/main.yml/badge.svg)](https://github.com/dj-wasabi/versiondb/actions/workflows/main.yml)


## How does it work

See []() to properly configure the container before proceding with the next steps.

When the API is running, we can do the following:

1. Authenticate yourself first.
2. Create an artifact by posting data to the `http://$URL:5001/api/v1/artifacts/`
3. 




### Authenticate




### Create artifact

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

| Property (type) | Description |
|-----------------|-------------|
| `name` (str) | The name of the artifact.|
| `category` (str) | The name of the category where this artifact belongs to. |
| `url` (str) | An url about the artifact. |
| `git` (str) | The url (https or git) to where the git repository is located. |
| `version` (str) | The initial version of the artifact to start with. |
| `metadata` (list) |  |

Both `version` (default `0.0.0`) as `metadata` are optional.


## Todo

Well, this isn't a finished product and still some things are to do to make the product more mature. Some of the following is still in the todo:

* Proper audit trail;
* Some endpoints should limit the amount of results with 'pages';
* Specify based on header what properties to show in sBOM;

