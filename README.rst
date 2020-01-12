forester
~~~~~~~~

Helpful scripts for the shell. These scripts were created for linux server maintenance,
filling small gaps left by the standard tools.

All scripts are written in pure Python and are platform-independent. So you can also
use them on Windows or Mac.

.. image:: https://img.shields.io/pypi/v/forester
  :alt: PyPI
  :target: https://pypi.org/project/forester/

.. image:: https://codecov.io/gh/chr1st1ank/forester/branch/master/graph/badge.svg
  :alt: codecov.io
  :target: https://codecov.io/gh/chr1st1ank/forester


Features
========
Offers commands to:

* Summarize the size and latest changes of folders in a directory tree
* List how much space the subfolders in a directory tree take when considering hardlinks between them

Pure Python. No dependencies - just the standard library.


Usage
=====

forester info
-------------

This command gets you an overview of folder contents. It shows the number of files and folders within each subfolder
as well as the newest modification time of any file within the subfolder.

.. code-block:: console

    $ forester info --max-depth=1 /usr
    Scanned 7909 folders

    Folder                                                 # Folders        # Files              m_time
    ----------------------------------------------------------------------------------------------------
    src                                                            1              0 2014-02-24 08:35:16
    share                                                      2,992         66,927 2019-12-26 23:57:06
    local                                                         24             71 2020-01-12 02:22:42
    lib32                                                          1              7 2019-11-17 22:11:33
    lib                                                        4,126         40,189 2020-01-12 09:53:20
    include                                                      757         15,106 2019-12-26 23:55:09
    bin                                                            7          2,306 2020-01-12 09:53:20
    ====================================================================================================
    .                                                          7,909        124,608 2020-01-12 09:53:20

forester contribs
-----------------

This command details out how much space is taken by each subfolder within a specified
directory.

.. code-block:: console

    $ forester contribs /mnt/backup2/incremental/
    Scanned 1115109 inodes
    Folder                                        Total size (B)     Size of unique inodes (B)
    ------------------------------------------------------------------------------------------
    2020-01-03                                   549,046,832,496                24,730,165,983
    2020-01-04                                   549,142,789,908                24,768,159,392
    2020-01-05                                   549,257,074,836                24,823,144,884
    2020-01-07                                   549,523,882,623                24,852,989,570
    2020-01-06                                   549,359,066,748                24,869,062,127
    2020-01-08                                   549,569,521,773                24,898,430,500
    2020-01-09                                   549,614,758,102                24,942,556,198
    2020-01-10                                   549,651,082,519                24,977,909,521
    2020-01-11                                   549,688,306,955                25,014,918,365
    2020-01-12                                   549,725,397,716                25,060,355,207
    2020-01-01                                   548,898,277,694                25,743,259,501
    ==========================================================================================
    Total                                        799,506,813,350                             -


There are two measures shown for each folder:

 - Total size: This is the total size of all files within the folder as it is also
   returned by `du`.
 - Size of unique inodes: This is the size of the inodes which are only linked into
   this folder. This excludes all files which are also hardlinked to one of the other
   listed folders. When deleting a folder this is the space which would be gained.

This command was created to measure how much space is taken by each snapshot within a folder
with incremental backups created by `rsync`.
Each folder contains hardlinks to the previous backups for unchanged files. With
`forester contribs` one can see how much space is exclusively taken by one of the
snapshots.


Installation
============
Forester is available on Pypi. Therefore installation is as straight forward as:

.. code-block:: sh

    pip install forester


Contributing
============
Interested in particular changes? Found a bug?
Please read `CONTRIBUTING.md <https://github.com/chr1st1ank/forester/CONTRIBUTING.md>`__
for instructions on how to participate.


License
=======
The code in this repository is made available freely and without warranty under the
terms of the MIT license (see `LICENSE <https://github.com/chr1st1ank/forester/LICENSE>`__).
Feel free to use, change and distribute it.
