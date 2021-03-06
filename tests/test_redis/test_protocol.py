#!/usr/bin/env python
from .common import *
from pprint import pprint

def get_conn():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((nc.host(), nc.port()))
    s.settimeout(.3)
    return s

def _test(req, resp, sleep=0):
    s = get_conn()

    if isinstance(req, bytes):
        req = [req]

    for i in req:
        s.sendall(i)
        time.sleep(sleep)

    s.settimeout(.3)

    data = s.recv(10000)
    assert(data == resp)

def test_slow():
    req = b'*1\r\n$4\r\nPING\r\n'
    resp = b'+PONG\r\n'

    if large > 1000:
        sleep = 1
    else:
        sleep = .1

    _test(req, resp, sleep)

def test_pingpong():
    req = b'*1\r\n$4\r\nPING\r\n'
    resp = b'+PONG\r\n'
    _test(req, resp)

def test_quit():
    if nc.version() < '0.4.2':
        return
    req = b'*1\r\n$4\r\nQUIT\r\n'
    resp = b'+OK\r\n'
    _test(req, resp)

def test_quit_without_recv():
    if nc.version() < '0.4.2':
        return
    req = b'*1\r\n$4\r\nQUIT\r\n'
    resp = b'+OK\r\n'
    s = get_conn()

    s.sendall(req)
    s.close()
    info = nc._info_dict()
    #pprint(info)
    assert(info['ntest']['client_err'] == 1)

def _test_bad(req):
    s = get_conn()

    s.sendall(req)
    data = s.recv(10000)
    print(data)

    assert(b'' == s.recv(1000))  # peer is closed

def test_badreq():
    reqs = [
        # '*1\r\n$3\r\nPING\r\n',
        b'\r\n',
        # '*3abcdefg\r\n',
        b'*3\r\n*abcde\r\n',

        b'*4\r\n$4\r\nMSET\r\n$1\r\nA\r\n$1\r\nA\r\n$1\r\nA\r\n',
        b'*2\r\n$4\r\nMSET\r\n$1\r\nA\r\n',
        # '*3\r\n$abcde\r\n',
        # '*3\r\n$3abcde\r\n',
        # '*3\r\n$3\r\nabcde\r\n',
    ]

    for req in reqs:
        _test_bad(req)


def test_wrong_argc():
    s = get_conn()

    s.sendall(b'*1\r\n$3\r\nGET\r\n')
    assert(b'' == s.recv(1000))  # peer is closed
