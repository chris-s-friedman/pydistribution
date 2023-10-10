# pydistribution

<!-- markdownlint-disable -->
<p align="center">
  <a href="https://github.com/chris-s-friedman/pydistribution/blob/main/LICENSE"><img src="https://img.shields.io/github/license/chris-s-friedman/pydistribution.svg?style=flat-square"></a>
  <a href="https://github.com/marketplace/actions/super-linter"><img src="https://github.com/chris-s-friedman/pydistribution/workflows/Lint%20Code%20Base/badge.svg"></a>
  <a href="https://gitmoji.dev"><img src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg?style=flat-square" alt="Gitmoji"/>
</a>
</p>
<!-- markdownlint-enable -->

Generate random variates in python

## Installation

```sh
pip install git+https://github.com/chris-s-friedman/pydistribution@latest-release
```

## Usage

### Generate a random number

```py
from pydistribution.random import Random

# Set a seed
random = Random(seed = 12345678)

# Generate 10 random numbers using MINSTD LCG
[i for i in random.lcg_minstd(n = 10)]
```

## Developer Notes

### Releases

This repository is setup to take advantage of the
[d3b-release-maker](https://github.com/d3b-center/d3b-release-maker/).
Please follow the instructions there to build releases.

### Linting

This repository is setup to take advantage of the
[GitHub Super Linter](https://github.com/marketplace/actions/super-linter).
Of note are the markdownlint files and the pyproject.toml.

