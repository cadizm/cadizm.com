
Create a User
=============

```
POST /headspace/users/
```

The endpoint's post body requires `username` and optionally accepts a list of
`book_ids`. For each valid `book_id`, the associated book is added to the
user's library as an unread book. Invalid `book_id`'s are ignored.

Sample request body:

```
{
    "username", "jumanji",
    "book_ids": [
        17,
        2,
        137,
        42
    ]
}
```

Returns:
  - 201 Created on successful user creation
  - 400 Bad Request on existing `username`
  - 400 Bad Request on malformed JSON or invalid post body
  - 405 Method Not Allowed on bad HTTP method

In addition to HTTP status code, the response's body will include the newly
created user's `username` along with a list of accepted valid `book_ids` and
ignored `invalid_book_ids`.

Sample response bodies:

```
{
    "result": {
        "username": "batman",
        "book_ids" : [2, 17, 42],
        "invalid_book_ids" : [137]
    },
    "meta": {
        "status": 201
    }
}

{
    "meta": {
        "status": 400,
        "reason": "username jumanji already exists with user_id 22"
    }
}

{
    "meta": {
        "status": 400,
        "reason": "bad JSON"
    }
}
```

Create a Book
=============

```
POST /headspace/books/
```

The endpoint's post body requires both `title` and `author`. If the given
(`title`, `author`) pair already exists, the response returns status 400 with
a `reason` field indicating such.

Sample request body:

```
{
    "title": "Travels",
    "author": "Michael Crichton"
}
```

Returns:
  - 201 Created on successful book creation
  - 400 Bad Request on existing (`title`, `author`) pair
  - 400 Bad Request on malformed JSON or invalid post body
  - 405 Method Not Allowed on bad HTTP method

In addition to HTTP status code, the response's body will include the newly
created book's `id`. Or in the case of a bad request, a reason as to why the
book could not be created.

Sample response bodies:

```
{
    "result": {
        "title": "Travels",
        "author": "Michael Crichton",
        "book_id" : 2
    },
    "meta": {
        "status": 201
    }
}

{
    "meta": {
        "status": 400,
        "reason": "The Hitchhiker's Guide to the Galaxy by Douglas Adams already exists with book_id 42"
    }
}

{
    "meta": {
        "status": 400,
        "reason": "bad JSON"
    }
}
```

Add a Book as Unread to a User's Library
========================================

```
POST /headspace/users/:username/books/:book_id/
```

The endpoint requires a valid `username` and `book_id` as part of the path,
but does not require a post body. If either of `username` or `book_id` are
invalid, a response with status 400 is returned with `reason` indicating why.

Returns:
  - 201 Created on successful addition of book to user library
  - 400 Bad Request on invalid `username` or `book_id`
  - 405 Method Not Allowed on bad HTTP method

The response's body will contain status 200 for valid requests, and in other
cases, it will include an error status and reason as to why the book could not
be added to the user's library.

Sample response bodies:

```
{
    "meta": {
        "status": 200
    }
}

{
    "meta": {
        "status": 400,
        "reason": "bad book_id 137"
    }
}
```

Mark a User's Book as Read or Unread
====================================

```
PUT /headspace/users/:username/books/:book_id/read/
PUT /headspace/users/:username/books/:book_id/unread/
```

The endpoint requires a valid `username` and `book_id` as part of the path,
but does not require a post body. If either of `username` or `book_id` are
invalid, a response with status 400 is returned with `reason` indicating why.

Returns:
  - 200 Success on successfully marking the user's book as read or unread
  - 400 Bad Request on invalid `username` or `book_id`
  - 405 Method Not Allowed on bad HTTP method

The response's body will contain status 200 for valid requests, and in other
cases, it will include an error status and reason as to why the book could not
be added to the user's library.

Sample response bodies:

```
{
    "meta": {
        "status": 200
    }
}

{
    "meta": {
        "status": 400,
        "reason": "bad username robin"
    }
}
```

Delete a Book from a User's Library
===================================

```
DELETE /headspace/users/:username/books/:book_id/
```

The endpoint requires a valid `username` and `book_id` as part of the path,
but does not require a post body. If either of `username` or `book_id` are
invalid, a response with status 400 is returned with `reason` indicating why.

Returns:
  - 200 Success on successfully deleting the book from the user's library
  - 400 Bad Request on invalid `username` or `book_id`
  - 405 Method Not Allowed on bad HTTP method

The response's body will contain status 200 for valid requests, and in other
cases, it will include an error status and reason as to why the book could not
be deleted from the user's library.

Sample response bodies:

```
{
    "meta": {
        "status": 200
    }
}

{
    "meta": {
        "status": 400,
        "reason": "bad book_id 137"
    }
}
```

List all Books in a User's Library
==================================

```
GET /headspace/users/:username/books/
```

The endpoint requires a valid `username` as part of the path, but does not
require a post body. If `username` is invalid, a response with status 400 is
returned with `reason` indicating why.

The endpoint optionally accepts query parameters `author`, `read`, and `unread`
which filter by the passed parameters. The `author` parameter is considered a
match to a given author's name if it exists as a substring within a book's
`author` field.

The `read` and `unread` parameters are mutually exclusive and returns results
such that when `read` is passed, results have field `read` equal to true. And
when `unread` is passed, results have field `read` equal to false.

Returns:
  - 200 Success on valid `username`
  - 400 Bad Request on invalid `username` or `book_id`
  - 405 Method Not Allowed on bad HTTP method

The response's body will contain status 200 for valid requests, and in other
cases, it will include an error status and reason as to why the book could not
be deleted from the user's library.

Sample response bodies:

```
{
    "result": {
        "books" : [
            {
                "book_id": 42,
                "title": "The Hitchhiker's Guide to the Galaxy",
                "author": "Douglas Adams",
            },
            {
                "book_id": 2,
                "title": "Travels",
                "author": "Michael Crichton"
            }
        ]
    },
    "meta": {
        "status": 200
    }
}

{
    "meta": {
        "status": 400,
        "reason": "username robin not found"
    }
}
```
