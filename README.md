# Soccer Stats API

[![Build Status](https://api.travis-ci.org/passy/soccer-stats-backend.png?branch=master)](https://travis-ci.org/passy/soccer-stats-backend)

Backend for my soccer prediction app, using a dumb time-independend least-square
regression algorithm.

Using Numpy and Flask.


## Endpoints

    /v1/scores

* Accepted Methods: `POST`
* Request Payload: JSON

```
{"results": [
    {"teamHome":"BVB","teamAway":"HSV","goalsHome":2,"goalsAway":1},
    ...
]}
```

* Response: JSON

```
{
    "scores": {"BVB": 0.49999999999999978, "HSV": -0.49999999999999989},
    "errors": [3.3306690738754696e-16]
}
```
