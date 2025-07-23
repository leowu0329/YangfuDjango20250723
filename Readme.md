Install wkhtmltopdf on Ubuntu 22.04
=======================================
sudo apt update
sudo apt install wget
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
sudo apt install -f ./wkhtmltox_0.12.6.1-2.jammy_amd64.deb

測試
$ wkhtmltopdf --version
wkhtmltopdf 0.12.6 (with patched qt)

$ wkhtmltoimage --version
wkhtmltoimage 0.12.6 (with patched qt)