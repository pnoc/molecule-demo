import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_user_and_group_exists(host):
    grp = host.group('realworld')
    assert grp is not None
    usr = host.user('realworld')
    assert usr is not None
    assert 'realworld' in usr.groups
    assert usr.home == '/home/realworld'


def test_service(host):
    srv = host.service("realworld-server")
    assert srv.is_running
    assert srv.is_enabled


def test_api(host):
    cmd = host.run('curl -so /dev/null -w "%{http_code}" http://localhost:3000/api/articles')
    assert cmd.rc == 0
    assert cmd.stdout == '200'
