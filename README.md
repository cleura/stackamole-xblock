# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/cleura/stackamole-xblock/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                                                   |    Stmts |     Miss |      Cover |   Missing |
|--------------------------------------------------------------------------------------- | -------: | -------: | ---------: | --------: |
| stackamole/\_\_init\_\_.py                                                             |        2 |        0 |    100.00% |           |
| stackamole/admin.py                                                                    |       52 |        1 |     98.08% |        51 |
| stackamole/common.py                                                                   |      136 |        5 |     96.32% |223-224, 229, 238, 268 |
| stackamole/jobs.py                                                                     |       77 |        0 |    100.00% |           |
| stackamole/management/\_\_init\_\_.py                                                  |        0 |        0 |    100.00% |           |
| stackamole/management/commands/\_\_init\_\_.py                                         |        0 |        0 |    100.00% |           |
| stackamole/management/commands/reaper.py                                               |       13 |        0 |    100.00% |           |
| stackamole/management/commands/suspender.py                                            |       13 |        0 |    100.00% |           |
| stackamole/migrations/0001\_initial.py                                                 |        5 |        0 |    100.00% |           |
| stackamole/migrations/0002\_stacklog.py                                                |        6 |        0 |    100.00% |           |
| stackamole/migrations/0003\_blanks.py                                                  |        5 |        0 |    100.00% |           |
| stackamole/migrations/0004\_auto\_20190715\_1053.py                                    |        5 |        0 |    100.00% |           |
| stackamole/migrations/0005\_auto\_20190811\_1555.py                                    |        6 |        0 |    100.00% |           |
| stackamole/migrations/0006\_auto\_20200107\_1332.py                                    |        6 |        0 |    100.00% |           |
| stackamole/migrations/0007\_add\_delete\_by\_and\_delete\_age.py                       |        5 |        0 |    100.00% |           |
| stackamole/migrations/0008\_add\_database\_defaults\_for\_stack\_key\_and\_password.py |        4 |        0 |    100.00% |           |
| stackamole/migrations/0009\_add\_null\_true\_for\_key\_and\_password.py                |        4 |        0 |    100.00% |           |
| stackamole/migrations/0010\_add\_user\_foreign\_key.py                                 |       18 |        5 |     72.22% |     19-24 |
| stackamole/migrations/0011\_allow\_null\_for\_learner.py                               |        6 |        0 |    100.00% |           |
| stackamole/migrations/0012\_add\_suspend\_by.py                                        |        4 |        0 |    100.00% |           |
| stackamole/migrations/0013\_migrate\_app\_label.py                                     |       26 |       10 |     61.54% |15-29, 38-40 |
| stackamole/migrations/\_\_init\_\_.py                                                  |        0 |        0 |    100.00% |           |
| stackamole/models.py                                                                   |       62 |        0 |    100.00% |           |
| stackamole/openstack.py                                                                |       42 |        0 |    100.00% |           |
| stackamole/provider.py                                                                 |      254 |       21 |     91.73% |11-12, 80-82, 90, 97-106, 110-111, 117-118, 152, 159-160, 295-296 |
| stackamole/stackamole.py                                                               |      520 |       38 |     92.69% |263-271, 347, 374, 402-418, 534, 802, 813, 864-867, 875, 958, 1051, 1054-1062, 1065, 1113, 1163, 1192, 1208, 1220 |
| stackamole/tasks.py                                                                    |      465 |        9 |     98.06% |286-287, 505, 589, 592, 901-902, 923-924 |
| **TOTAL**                                                                              | **1736** |   **89** | **94.87%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/cleura/stackamole-xblock/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/cleura/stackamole-xblock/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/cleura/stackamole-xblock/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/cleura/stackamole-xblock/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fcleura%2Fstackamole-xblock%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/cleura/stackamole-xblock/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.