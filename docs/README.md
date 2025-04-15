# DOCUMENT / 文档 / ドキュメント

note that server will not storage all version of a entry ( I guess)

but will write to log when a entry was changed or created, and log will contain every thing for a entry (use its method to get one-line output)

(also can call a webhook if needed)

so if you want to build a history tree, you can use full log or webhook.

## SERVER API

* GET `/entry/["all"|condition]`

* GET `/entry/[id]`

* PUT `/entry/create`

will return 200 if create successful, or will return 403 if already created or 402 if created failed or 401 if server refused with unknown reason.

will get *** if your request don't match valid json format.

* POST `/entry/update/[id]`

this must update with version, if version don't match latest version+1, server will refuse to update because you are trying to change a already created version or future version.

will get 200 if update successful.

will get 404 if try to update a entry not found on server 

will get 403 if server refused to update for unknown version

will get 405 if you are trying to update history version

will get 407 if you are trying to update future version.

But, if with --future as True it will ignore warning and you also can set several blank version for version between server and you given.

will get *** if your request is not valid json format.

* DELETE `/entry/update/[id]`

must give a latest version if you want to delete a 

