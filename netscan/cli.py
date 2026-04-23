#!/usr/bin/env python3

from netscan import __version__
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import socket
import ipaddress
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
import logging
import csv
import json
import sys
import os
import threading
import subprocess
import platform
import time
from contextlib import nullcontext

# Configure logging
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s"
)

console = Console()

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3389: "RDP",
    3306: "MySQL",
    5432: "PostgreSQL",
    5900: "VNC",
    8000: "Dev Server",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    8888: "Jupyter",
    9200: "Elasticsearch",
    6379: "Redis",
    27017: "MongoDB",
    25565: "Minecraft Server",
}


def ping_host(ip, timeout=1):
    """Ping a host once using the system ping command. Returns True if host replies."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    timeout_param = "-w" if platform.system().lower() == "windows" else "-W"

    try:
        result = subprocess.run(
            [
                "ping",
                param,
                "1",
                timeout_param,
                (
                    str(int(timeout * 1000))
                    if platform.system().lower() == "windows"
                    else str(int(timeout))
                ),
                ip,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout + 1,  # subprocess-level safety timeout
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False


def scan_host(ip, ports=None, timeout=0.01):
    """Scan a given IP for a list of ports or a single port."""
    thread_name = threading.current_thread().name
    logging.debug(f"[{thread_name}] Scanning {ip} on ports {ports}")
    results = []
    for port in ports:
        try:
            logging.debug(f"Scanning IP {ip}, Port {port}")
            with socket.create_connection((str(ip), port), timeout=timeout):
                results.append((port, True))
        except (socket.timeout, ConnectionRefusedError, OSError):
            results.append((port, False))
    return results


def parse_ports(port_args):
    """Parse port tokens like ['22', '80,443', '8000-8010'] into a sorted list."""
    if not port_args:
        return None

    ports = set()
    for token in port_args:
        for item in token.split(","):
            item = item.strip()
            if not item:
                continue

            if "-" in item:
                start_text, end_text = item.split("-", 1)
                try:
                    start = int(start_text)
                    end = int(end_text)
                except ValueError as exc:
                    raise ValueError(f"Invalid port range '{item}'") from exc

                if start > end:
                    raise ValueError(
                        f"Invalid port range '{item}'. Range start must be <= end."
                    )
                if start < 1 or end > 65535:
                    raise ValueError(
                        f"Invalid port range '{item}'. Ports must be between 1 and 65535."
                    )
                ports.update(range(start, end + 1))
                continue

            try:
                port = int(item)
            except ValueError as exc:
                raise ValueError(f"Invalid port '{item}'") from exc

            if port < 1 or port > 65535:
                raise ValueError(
                    f"Invalid port number '{port}'. Port must be between 1 and 65535."
                )
            ports.add(port)

    return sorted(ports)


def sort_results(results):
    """Sort scan results deterministically by IP and port."""
    sorted_results = []
    for ip, hostname, port_results in sorted(
        results, key=lambda item: ipaddress.ip_address(item[0])
    ):
        sorted_port_results = sorted(
            port_results,
            key=lambda item: (-1 if item[0] is None else item[0]),
        )
        sorted_results.append((ip, hostname, sorted_port_results))
    return sorted_results


def results_to_json_ready(results, show_all=False):
    """Convert scan results into a JSON-serializable structure."""
    payload = []
    for ip, hostname, port_results in results:
        ports = []
        for port, status in port_results:
            if not show_all and not status:
                continue
            ports.append(
                {
                    "port": port,
                    "service": COMMON_PORTS.get(port, "Unknown"),
                    "up": status,
                    "status": "Up" if status else "Down",
                }
            )
        payload.append({"ip": ip, "hostname": hostname, "ports": ports})
    return payload


def write_csv(results, output_csv):
    """Write results to CSV."""
    folder_path = os.path.dirname(output_csv)
    if folder_path and not os.path.exists(folder_path):
        raise FileNotFoundError(f"The directory '{folder_path}' does not exist.")

    with open(output_csv, mode="w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["IP Address", "Hostname", "Port", "Service", "Status"])
        for ip, hostname, port_results in results:
            for port, status in port_results:
                service = COMMON_PORTS.get(port, "Unknown")
                csv_writer.writerow([ip, hostname, port, service, "Up" if status else "Down"])


def scan_network(
    network_cidr, ports=None, timeout=0.5, max_workers=100, show_progress=True
):
    """
    Scan all hosts in a given CIDR network.
    - If ports is None, it performs ICMP ping-only to detect live hosts.
    - Otherwise, it scans the given TCP ports per host.
    """
    results = []
    net = ipaddress.ip_network(network_cidr, strict=False)
    ip_list = list(net.hosts())

    progress_context = Progress() if show_progress else nullcontext()
    with progress_context as progress:
        task = progress.add_task("[cyan]Scanning...", total=len(ip_list)) if show_progress else None

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            if ports is None:
                # ICMP ping-only mode
                future_to_ip = {
                    executor.submit(ping_host, str(ip), timeout): str(ip)
                    for ip in ip_list
                }
                for future in as_completed(future_to_ip):
                    ip = future_to_ip[future]
                    is_up = future.result()
                    hostname = resolve_hostname(ip) if is_up else "-"
                    results.append((ip, hostname, [(None, is_up)]))
                    if show_progress:
                        progress.update(task, advance=1)
            else:
                # TCP port scan mode
                future_to_ip = {
                    executor.submit(scan_host, str(ip), ports, timeout): str(ip)
                    for ip in ip_list
                }
                for future in as_completed(future_to_ip):
                    ip = future_to_ip[future]
                    try:
                        port_results = future.result()
                    except Exception as e:
                        logging.warning(f"Error scanning {ip}: {e}")
                        port_results = []
                    hostname = resolve_hostname(ip)
                    results.append((ip, hostname, port_results))
                    if show_progress:
                        progress.update(task, advance=1)

    return results


def display_results(results, show_all=False):
    """Display scan results using a rich table."""
    table = Table(title="Scan Results")
    table.add_column("IP Address", style="bold")
    table.add_column("Hostname", style="cyan")
    table.add_column("Port", style="magenta")
    table.add_column("Service", style="yellow")
    table.add_column("Status", style="green")

    for ip, hostname, port_results in results:
        for port, status in port_results:
            if not show_all and not status:
                continue
            service = COMMON_PORTS.get(port, "Unknown")
            table.add_row(
                ip, hostname, str(port), service, "🟢 Up" if status else "🔴 Down"
            )

    console.print(table)


def resolve_hostname(ip):
    """Try to resolve the hostname of an IP address."""
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except socket.herror:
        return "-"


def build_parser():
    parser = argparse.ArgumentParser(
        prog="netscan",
        description="Simple network scanner",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "network",
        help="CIDR network range to scan (e.g., 192.168.1.0/24) or a simple hostname",
    )

    parser.add_argument(
        "-v", "--version", action="version", version=f"netscan {__version__}"
    )

    parser.add_argument(
        "-p",
        "--port",
        nargs="*",
        help="TCP port(s) to scan. Supports values like 80 443, 80,443, or 8000-8010",
    )
    parser.add_argument(
        "--common-ports",
        action="store_true",
        help="Scan a list of common ports (e.g., FTP, SSH, HTTP, etc.). Common ports include: 21 (FTP), 22 (SSH), 23 (Telnet), 25 (SMTP), 53 (DNS), 80 (HTTP), 110 (POP3), 139 (NetBIOS), 143 (IMAP), 443 (HTTPS), 445 (SMB), 3389 (RDP), 3306 (MySQL), 5432 (PostgreSQL), 5900 (VNC), 8000 (Dev Server), 8080 (HTTP-Alt), 8443 (HTTPS-Alt), 8888 (Jupyter), 9200 (Elasticsearch), 6379 (Redis), 27017 (MongoDB), 25565 (Minecraft Server).",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=0.5,
        help="Connection timeout in seconds",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose mode for detailed logs"
    )
    parser.add_argument(
        "--output-csv", type=str, help="Path to output results in CSV format"
    )
    parser.add_argument(
        "--show-all",
        action="store_true",
        help="Show all results, including closed ports",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=100,
        help="Maximum number of concurrent host scan workers",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output scan results as JSON",
    )
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Verbose mode enabled")
    else:
        logging.getLogger().setLevel(logging.WARNING)

    logging.debug(f"Arguments: {args}")

    # Validate network or hostname argument
    try:
        # Check if it's a valid IP network
        ipaddress.ip_network(args.network, strict=False)
    except ValueError:
        # If not, check if it's a valid hostname
        try:
            resolved_ip = socket.gethostbyname(args.network)
            console.print(
                f"[bold blue]Resolved hostname '{args.network}' to IP '{resolved_ip}'[/bold blue]"
            )
            args.network = resolved_ip + "/32"  # Treat as a single-host network
        except socket.gaierror:
            console.print(
                f"[bold red]Error: Invalid network range or hostname '{args.network}'[/bold red]"
            )
            return 1

    try:
        parsed_ports = parse_ports(args.port)
    except ValueError as exc:
        console.print(f"[bold red]Error: {exc}[/bold red]")
        return 1

    # Validate timeout argument
    if args.timeout <= 0:
        console.print("[bold red]Error: Timeout must be a positive number.[/bold red]")
        return 1
    if args.workers <= 0:
        console.print("[bold red]Error: Workers must be a positive integer.[/bold red]")
        return 1

    ports = (
        list(COMMON_PORTS.keys())
        if args.common_ports
        else parsed_ports
    )
    if not args.json and ports is None:
        console.print(
            f"[bold blue]Scanning {args.network} with ping (no ports specified) with timeout {args.timeout}s[/bold blue]"
        )
    elif not args.json:
        console.print(
            f"[bold blue]Scanning {args.network} on ports {ports} with timeout {args.timeout}s using {args.workers} workers[/bold blue]"
        )

    # Start scanning
    start = time.time()
    results = sort_results(
        scan_network(
            args.network,
            ports=ports,
            timeout=args.timeout,
            max_workers=args.workers,
            show_progress=not args.json,
        )
    )
    duration = time.time() - start

    if args.json:
        payload = {
            "network": args.network,
            "mode": "ping" if ports is None else "tcp",
            "ports_requested": ports,
            "timeout": args.timeout,
            "workers": args.workers,
            "duration_seconds": round(duration, 4),
            "results": results_to_json_ready(results, show_all=args.show_all),
        }
        console.print_json(data=payload)
    else:
        console.print(
            f"[bold green]Scan completed in {duration:.2f} seconds[/bold green]"
        )
        display_results(results, show_all=args.show_all)

    # If output CSV is specified, write results to CSV
    if args.output_csv:
        try:
            write_csv(results, args.output_csv)
        except Exception as e:
            console.print(f"[bold red]Error writing CSV: {e}[/bold red]")
            return 1

        if not args.json:
            console.print(f"[bold green]Results written to {args.output_csv}[/bold green]")

    return 0


if __name__ == "__main__":
    sys.exit(main())
