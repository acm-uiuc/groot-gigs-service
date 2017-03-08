# groot-gig-service

Groot core development:

[![Join the chat at https://gitter.im/acm-uiuc/groot-development](https://badges.gitter.im/acm-uiuc/groot-development.svg)](https://gitter.im/acm-uiuc/groot-development?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Questions on how to add your app to Groot or use the Groot API:

[![Join the chat at https://gitter.im/acm-uiuc/groot-users](https://badges.gitter.im/acm-uiuc/groot-users.svg)](https://gitter.im/acm-uiuc/groot-users?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


Supporting the Groot economy 

## Install / Setup
1. Clone repo:

    ```
    git clone https://github.com/acm-uiuc/groot-gig-service
    cd groot-gig-service
    ```

2. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

3. Copy settings template:

    ```
    cd groot_gig_service
    cp settings.template.py settings.py
    ```

4. Add your DB credentials to settings.py.

## Run Application
```
python app.py
```

## Routes

### Gig Routes

#### GET /gigs

Returns list of gigs.

Each gig "looks like":

```
{
    "active": true,
    "created_at": "2017-03-06T14:15:10",
    "credits": 1.23,
    "description": "Clean up the office",
    "id": 12345,
    "issuer": "bcongdo2"
}
```

#### GET /gigs/:gig_id

Returns information about a specific gig.

Each gig "looks like":

```
{
    "active": true,
    "created_at": "2017-03-06T14:15:10",
    "credits": 1.23,
    "description": "Clean up the office",
    "id": 12345,
    "issuer": "bcongdo2"
}
```

#### POST /gigs

Endpoint for creating a Gig 

*Body Params:*

* `issuer` - NetID of the user being creating the Gig
    * Required
* `description` - Description of the gig
* `credits` - Amount of credits being offered for the gig
    * Required
    * Type: Float
* `admin_task` - If True, then credits are created when Claim is fulfilled. If False, then credits are deducted from the issuer when Claim is fulfilled
    * Default: False

#### PUT /gigs/:gig_id

Endpoint for activating/deactivating a gig

*Body Params:*

* `active` - New state of the Gig
    * Required
    * Type: Bool

#### DELETE /gigs/:gig_id

Deletes the specified Gig.

### Claim Routes

#### GET /gigs/claims

Returns list of claims.

*URL Params:*
* `gig_id` - Filter by associated gig id
    * Optional
    * Type: Int

Each claim "looks like":

```
{
    "claimant": "bcongdo2",
    "created_at": "2017-03-06T15:26:45",
    "fulfilled": false,
    "gig_id": 5,
    "id": 2
}
```

#### POST /gigs/claims

Endpoint for creating a claim

*Body Params:*

* `claimant` - NetID of user making claim
    * Required
* `gig_id` - ID of gig being claimed
    * Required
    * Type: int

#### PUT /gigs/claims/:claim_id

Endpoint for fulfilling a claim

#### DELETE /gigs/claims/:claim_id

Endpoint for deleting a claim. Creates transactions to transfer credits to claimant as necessary.

## Contributing

Contributions to `groot-gig-service` are welcomed!

1. Fork the repo.
2. Create a new feature branch.
3. Add your feature / make your changes.
4. Install [pep8](https://pypi.python.org/pypi/pep8) and run `pep8 *.py` in the root project directory to lint your changes. Fix any linting errors.
5. Create a PR.
6. ???
7. Profit.
