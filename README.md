# VersionDB

_Why?_

I needed a place to store versions of libraries or applications, without storing the actual artifacts. That place would allow me to add/update information in an automated way from the CI/CD pipeline. A central place containing all the artifacts to generate a sBOM based on a group or category. A sBOM that I then also could version as well.

VersionDB helps to achieve this. An API where you can an artifact, and as part of the CI/CD pipeline a version can stored. Once you have added a version, you can add/update information for extra validation like a commit or an hash. Any of these information sources can be used with the generation of the sBOM.

[![MasterRun](https://github.com/dj-wasabi/versiondb/actions/workflows/main.yml/badge.svg)](https://github.com/dj-wasabi/versiondb/actions/workflows/main.yml)


## How does it work

First, the product is in very early stages. :) Same as the documentation.. :)

See []() to properly configure the container before proceding with the next steps.

When the API is running, we can do the following:

1. Authenticate yourself first.
2. Create an artifact by posting data to the `http://$URL:5001/api/v1/artifacts/`
3. 




### Authenticate

An admin user is created with the start and we need to use these credentials to start with. In the following example credentials are used from the `docker-compose.yml` file:

```sh
$ curl -XPOST -d '{"username": "admin", "password": "admin"}' http://localhost:5001/api/v1/users/authenticate | jq .
{
    "token": "eyJmcmVzaCI6ZmFsc2..."
}
```

With every request that follows, a header needs to be provided. Example with curl:

```sh
$ curl -H 'Authorization: Bearer eyJmcmVzaCI6ZmFsc2...' http://localhost:5000/api/v1/*
```

### Create artifact

The following provides an example of a json data that is needed to create an artifact:
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

Post the following to `http://$URL:5001/api/v1/artifacts/`

```sh
$ curl -XPOST -d '@artifact.json' -H 'Authorization: Bearer eyJmcmVzaCI6ZmFsc2...' http://localhost:5000/api/v1/artifacts | jq .
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

## Todo

Well, this isn't a finished product and still some things are to do to make the product more mature. Some of the following is still in the todo:

* Proper audit trail;
* Adding usergroups to categories to limit access and possibilities;
* Some endpoints should limit the amount of results with 'pages';
* Specify based on header what properties to show in sBOM;
* Not be able to register an account;

## Development

A `docker-compose.dev.yml` can be used for development purposes. It will mount the `src/` directory in the container and it will reload once files are updated. When you have a feature or want to fix a bug, you can devel and test it with this way.

Once you are happy, you can create a Pull Request and once everything looks fine I will merge it.
