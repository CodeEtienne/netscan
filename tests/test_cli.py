import json

from netscan import cli


def test_parse_ports_supports_lists_ranges_and_dedupes():
    assert cli.parse_ports(["22", "80,443", "8000-8002", "443"]) == [
        22,
        80,
        443,
        8000,
        8001,
        8002,
    ]


def test_parse_ports_rejects_invalid_range():
    try:
        cli.parse_ports(["100-90"])
    except ValueError as exc:
        assert "Range start must be <= end" in str(exc)
    else:
        raise AssertionError("Expected parse_ports to reject descending ranges")


def test_main_passes_workers_and_ports(monkeypatch):
    captured = {}

    def fake_scan_network(network_cidr, ports=None, timeout=0.5, max_workers=100, show_progress=True):
        captured["network"] = network_cidr
        captured["ports"] = ports
        captured["timeout"] = timeout
        captured["max_workers"] = max_workers
        captured["show_progress"] = show_progress
        return [("127.0.0.1", "localhost", [(22, True), (80, False)])]

    monkeypatch.setattr(cli, "scan_network", fake_scan_network)

    exit_code = cli.main(["127.0.0.1/32", "-p", "22,80", "--workers", "12"])

    assert exit_code == 0
    assert captured == {
        "network": "127.0.0.1/32",
        "ports": [22, 80],
        "timeout": 0.5,
        "max_workers": 12,
        "show_progress": True,
    }


def test_main_json_output(monkeypatch, capsys):
    def fake_scan_network(network_cidr, ports=None, timeout=0.5, max_workers=100, show_progress=True):
        return [("127.0.0.1", "localhost", [(22, True), (80, False)])]

    monkeypatch.setattr(cli, "scan_network", fake_scan_network)

    exit_code = cli.main(["127.0.0.1/32", "-p", "22,80", "--workers", "4", "--json", "--show-all"])

    assert exit_code == 0
    stdout = capsys.readouterr().out
    payload = json.loads(stdout)
    assert payload["network"] == "127.0.0.1/32"
    assert payload["mode"] == "tcp"
    assert payload["ports_requested"] == [22, 80]
    assert payload["workers"] == 4
    assert payload["results"] == [
        {
            "ip": "127.0.0.1",
            "hostname": "localhost",
            "ports": [
                {"port": 22, "service": "SSH", "up": True, "status": "Up"},
                {"port": 80, "service": "HTTP", "up": False, "status": "Down"},
            ],
        }
    ]


def test_main_rejects_invalid_workers():
    assert cli.main(["127.0.0.1/32", "--workers", "0"]) == 1
