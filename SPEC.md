# Wellfed specification

In order to expose metadata about a server (later called a manifest), one must
expose a JSON structured object by:

- conforming to the specification for exposing the object;
- conforming to the specification for the object content.

# What a manifest is about

A manifest is about exposing metadata regarding a server instance in a
federation. The purpose of manifests is to be able to display metadata to
users in a useful way in clients, and to help third parties crawl metadata from
participating servers and display meaningful server lists.

A manifest is not about exposing technical data specific to a federation, and
will thus not contain information about a server implementation, protocol or
version.

# Exposing a manifest

## For a Matrix server

A Matrix server *may* expose a manifest by serving it at
``GET /_matrix/client/manifest``.

## For a Mastodon server

A Mastodon server *may* expose a manifest by service it at
``GET /api/v1/instance``.

## For a website

A website *may* expose a manifest at ``/manifest.json`` in the web root.

A website *may* expose a manifest at an arbitrary URI, provided it embeds
a link in the ``head`` section of its homepage:

```
<link rel="manifest" type="application/json" href="path/to/manifest.json">
```

## For a mail server

A mailserver *may* expose a manifest by announcing its Web URI in the server
banner.

# Structure of a manifest

A manifest is JSON object including a single top-level ``application/json``
key, including an object with any subset of the following keys.

Example :

```json
{
  "application/json": {
    "owners": [],
  }
}
```

## ``federation`` (type: string)

One of the valid federation types:
- ``mail``, the global mail service federation
- ``matrix``, the [Matrix](https://matrix.org) federation
- ``jabber``, the [Jabber XMPP](https://xmpp.org) federation
- ``mastodon``, the [Mastodon](https://joinmastodon.org/) fediverse
- ``diapora``, the [Diaspora](https://diasporafoundation.org/) federation
- ``none``, any service that is related to a federation but not actively part
  of one.

Exposing manifests for services other than federations has two purposes:
displaying some features that are common to federations and other services, and
being properly referenced when it is mentioned as a relation in a federated
service.

## ``owners`` (type: list of dictionaries)

Each dictionary represents a co-owner of the server.

Each dictionary contains the following fields:
- ``type``, one of the predefined owner types
- ``name``, name of the owner as a string

Valid owner types are:
- ``person``, a physical person
- ``nonprofit``, a non profit foundation or other nonprofit entity
- ``company``, a commercial Company
- ``state``, a state-owned entity or a government entity

Example:

```json
"owners": [
  {
    "type": "person",
    "name": "John Doe"
  },
  {
    "type": "person",
    "name": "Jane Doe"
  },
  {
    "type": "nonprofit",
    "name": "Example Foundation"
  }
]
```

## ``related`` (type: list of dictionaries)

Each dictionary represents a related federated service.

Each dictionary contains the following fields:
- ``federation``, one of the predefined federation types (see ``federation``)
- ``relation``, one of the predefined relation types
- ``server``, the server address
- ``name``, the server name

Valid relations are:
- ``owned``, the server is owned by one of this server owners
- ``friend``, server owners are friends
- ``partner``, server owners are business partners
- ``helped``, this server owners help the other server owners
- ``helping``, this server owners are helped by the other server owners

Example:

```json
"related": [
  {
    "federation": "matrix",
    "relation": "friend",
    "server": "matrix.org",
    "name": "Matrix dot org main server"
  },
  {
    "federation": "mail",
    "relation": "owned",
    "server": "domain.tld",
    "name": "Our mail service"
  }
]
```

## ``languages`` (type: list of strings)

Each string in the list is the ISO639-1 code for one of the main languages
spoken on the server.

Example :

```json
"languages": [
  "fr",
  "en",
  "de"
]
```

## ``locations`` (type: list of strings)

Each string in the list is the alpha2 ISO3166-1 code for a country this server
is technically or administratively related to.

Example:

```json
"locations": [
  "fr",
  "gb"
]
```

## ``description`` (type: markdown string)

Description of the server, using markdown for formatting.

Example:

```json
"description": "This is the *main* server for [our community](domain.tld)."
```

## ``rules`` (type: markdown string)

Set of rules for this server, using markdown for formatting.

Example:

```json
"rules": "One **shall not** kill."
```

## ``tags`` (type: list of strings)

Each string in the list is a short tag (lowercase alpha plus hyphen, maximum
length of 50 characters) describing a feature, an ideology, any concept that
this server is related to.

Example :

```json
"tags": ["programming", "federation", "socialist", "open-minded"]
```

## ``public`` (type: boolean)

Whether this server should be displayed in public lists.

Example:

```json
"public": true
```

## ``registration`` (type: string)

One of:
- ``open``, open to any registration,
- ``support``, registration requires that one first contacts the support team
- ``external``, registration is bound to another resource
- ``closed``, registration is closed, one should not register

Example :

```json
"registration": "support"
```

## ``deletion`` (type: string)

One of:
- ``none``, no account deletion is permitted
- ``suspend``, account can be suspended
- ``delete``, account and associated data can be deleted
- ``support``, deletion requires that one first contacts the support team

## ``reliability`` (type: dictionary)

The dictionary keys are picked among:
- ``availability`` for general day to day availability
- ``durability`` for the confidence in long term management
- ``security`` from a technical security point of view
- ``privacy`` for more general privacy concerns, including legal ones

Dictionary values are scores as integers bound between ``0`` (no confidence)
and ``5`` (full confidence).

Example :

```json
"reliability": {
  "availability": 4,
  "privacy": 3,
  "durability": 5
}
```

## ``size`` (type: dictionary)

The dictionary keys are picked among:
- ``rooms``, number of rooms if applicable
- ``users``, number of local users if applicable (not including service and
  bridged users)
- ``services``, number of service users if applicable, includes bots and
  bridged users
- ``links``, number of links to other servers in the federation

Dictionary values are integers representing the number directly.

Example :

```json
"size": {
  "users": 139,
  "services": 841,
  "links": 12
}
```

## ``features`` (type: list of dictionaries)

Each dictionary represent a feature supported by the server.

Each dictionary contains the following fields:
- ``type``: among a predefined list of types,
- ``name``: name of the feature,
- ``resource``: optional resources for this feature (URI, address, etc.)

Valid feature types are:
- ``bridge``, a bridge to another network or federation,
- ``voip``, VoIP conferencing,
- ``files``, file hosting service,
- ``webclient``, a Web client to access the server
- ``backup``, exportable account backups
- ``migration``, a data migration service
- ``other``, any additional feature

Example :

```json
"features": [
  {
    "type": "bridge",
    "name": "IRC bridge",
  },
  {
    "type": "webclient",
    "name": "Riot Web client",
    "resources": ["https://domain.tld/riot/"]
  }
]
```

## ``contacts`` (type: list of dictionaries)

Each dictionary in the list represents a contact for the server.

Each dictionary contains the following fields:
- ``type``, among a predefined list of types,
- ``name``: name of the contact,
- ``resource``: optional resources for this contact, (URI, address, phone, etc.)

Valid types are:
- ``administrative``, for administrative discussions
- ``technical``, for technical discussion between administrators
- ``support``, for technical user support
- ``commercial``, for commercial support and discussions
- ``legal``, for legal requests

Example :

```json
"contacts": [
  {
    "type": "technical",
    "name": "John Doe",
    "resources": ["john.doe@domain.tld", "+0012345678"]
  },
  {
    "type": "legal",
    "name": "Company Ltd.",
    "resources": ["legal@domain.tld", "https://domain.tld/legal"]
  }
]
```

## ``entrypoints`` (type: list of dictionaries)

Each dictionary in the list is an entrypoint to browse the server.

Each dictionary contains the following fields:
- ``name``: name of the category
- ``items``: list of rooms, users, any items in that category
- ``children``: optional list of subcategories, as similar dictionaries

Example :

```json
"entrypoints": [
  {
    "name": "Main topics",
    "items": ["room1@server1", "room2@server2"],
    "children": [
      {
        "name": "Topic A",
        "items": ["room3@server1", "room4@server"]
      },
      {
        "name": "Topic B",
        "items": ["room5@server1", "room6@server"]
      }
    ]
  }
]
```
