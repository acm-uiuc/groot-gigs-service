# groot-gig-service
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

#### GET /gigs/:gig_id

Returns information about a specific gig.

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

#### POST /gigs/claims

#### PUT /gigs/claims/:claim_id

#### DELETE /gigs/claims/:claim_id

## Contributing

Contributions to `groot-gig-service` are welcomed!

1. Fork the repo.
2. Create a new feature branch.
3. Add your feature / make your changes.
4. Install [pep8](https://pypi.python.org/pypi/pep8) and run `pep8 *.py` in the root project directory to lint your changes. Fix any linting errors.
5. Create a PR.
6. ???
7. Profit.