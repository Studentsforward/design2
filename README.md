# Compile Python (3.6)
Python 3 does not come with SSL support natively, so we have to compile it ourselves -- this allows us to interact with plaid and facebook authentication securely.
## OS X

    brew install openssl
    wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz
    tar xvzf Python-3.6.0.tgz

inside of `Modules/Setup.dist` find and change:

    SSL=/usr/local/Cellar/openssl/<version #>
    # uncomment next block

Configure and make:

    LDFLAGS="-L/usr/local/opt/sqlite/lib" CPPFLAGS="-I/usr/local/opt/sqlite/include" ./configure --enable-loadable-sqlite-extensions --prefix=/usr/local --enable-shared
    make
    make install

## Linux (Redhat)

    sudo yum install gcc openssl openssl-devel
    wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz
    tar xvzf Python-3.6.0.tgz

Find where openssl headers are.

    find / -name openssl
    > /usr/include/openssl

Take the base before /include/openssl, in this case `/usr`

Modify `Modules/Setup.dist`:

    SSL=/usr
    # uncomment the next few lines beginning with _ssl

Make and install:

    ./configure --enable-loadable-sqlite-extensions
    make
    make install
