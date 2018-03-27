
function install_venv {
    echo '#### install venv ######'
    pip install virtualenv
    virtualenv --no-site-packages venv
}

if [ ! -d ./venv ]
then
    install_venv
fi