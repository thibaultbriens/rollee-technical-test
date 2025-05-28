# Welcome to my technical test for Rollee

## To launch the server

`python manage.py migrate`
`python manage.py runserver`

## API endpoints:

### Quiz

Endpoint:
`/quiz?url=<wikipedia_url>` (default to python programing language)

Result:

```{
    "title": "Python (programming language)",
    "paragraphs": [
            ...
        ]
}
```
