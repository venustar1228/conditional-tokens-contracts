Gnosis Smart Contracts
===================

[![Logo](assets/logo.png)](https://gnosis.pm/)

[![Slack Status](https://slack.gnosis.pm/badge.svg)](https://slack.gnosis.pm)

Collection of smart contracts for the Gnosis prediction market platform (https://www.gnosis.pm).
To interact with those contracts have a look at (https://github.com/gnosis/gnosis.js/).

Install
-------------
### Install requirements with npm:
```
npm install
```

Test
-------------
### Run all tests (requires Node version >=7 for `async/await`):
```bash
npm test
```

Compile and Deploy
------------------
### Compile all contracts to obtain ABI and bytecode:
```bash
npm run compile
```

### Migrate all contracts required for the basic framework onto network associated with RPC provider:
```bash
npm run migrate
```

### Clean up network artifacts for networks not named in `truffle.js`
```bash
npm run netclean
```

Security and Liability
-------------
All contracts are WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

License
-------------
All smart contracts are released under GPL v.3.

Contributors
-------------
- Stefan George ([Georgi87](https://github.com/Georgi87))
- Martin Koeppelmann ([koeppelmann](https://github.com/koeppelmann))
- Alan Lu ([cag](https://github.com/cag))
- Roland Kofler ([rolandkofler](https://github.com/rolandkofler))
- Collin Chen ([collinc97](https://github.com/collinc97))
