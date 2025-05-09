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
import sys
import os
import threading
import subprocess
import platform
import time

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


def scan_network(network_cidr, ports=None, timeout=0.5, max_workers=100):
    """
    Scan all hosts in a given CIDR network.
    - If ports is None, it performs ICMP ping-only to detect live hosts.
    - Otherwise, it scans the given TCP ports per host.
    """
    results = []
    net = ipaddress.ip_network(network_cidr, strict=False)
    ip_list = list(net.hosts())

    with Progress() as progress:
        task = progress.add_task("[cyan]Scanning...", total=len(ip_list))

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


def main():
    parser = argparse.ArgumentParser(
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
        type=int,
        nargs="*",
        help="TCP port(s) to scan (e.g., -p 80 443)",
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
        help="Connection timeout in seconds (default: 0.01)",
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

    args = parser.parse_args()

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
            sys.exit(1)

    # Validate port argument
    if args.port:
        for port in args.port:
            if port < 1 or port > 65535:
                console.print(
                    f"[bold red]Error: Invalid port number '{port}'. Port must be between 1 and 65535.[/bold red]"
                )
                sys.exit(1)

    # Validate timeout argument
    if args.timeout <= 0:
        console.print("[bold red]Error: Timeout must be a positive number.[/bold red]")
        sys.exit(1)

    ports = (
        list(COMMON_PORTS.keys())
        if args.common_ports
        else (args.port if args.port else None)
    )
    if ports is None:
        console.print(
            f"[bold blue]Scanning {args.network} with ping (no ports specified) with timeout {args.timeout}s[/bold blue]"
        )
    else:
        console.print(
            f"[bold blue]Scanning {args.network} on ports {ports} with timeout {args.timeout}s[/bold blue]"
        )

    # Start scanning
    start = time.time()
    results = scan_network(args.network, ports=ports, timeout=args.timeout)
    console.print(
        f"[bold green]Scan completed in {time.time() - start:.2f} seconds[/bold green]"
    )
    display_results(results, show_all=args.show_all)

    # If output CSV is specified, write results to CSV
    if args.output_csv:
        folder_path = os.path.dirname(args.output_csv)
        if folder_path and not os.path.exists(folder_path):
            console.print(
                f"[bold red]Error: The directory '{folder_path}' does not exist.[/bold red]"
            )
            sys.exit(1)
        try:
            with open(args.output_csv, mode="w", newline="") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(
                    ["IP Address", "Hostname", "Port", "Service", "Status"]
                )
                for ip, hostname, port_results in results:
                    for port, status in port_results:
                        service = COMMON_PORTS.get(port, "Unknown")
                        csv_writer.writerow(
                            [ip, hostname, port, service, "Up" if status else "Down"]
                        )
            console.print(
                f"[bold green]Results written to {args.output_csv}[/bold green]"
            )
        except Exception as e:
            console.print(f"[bold red]Error writing CSV: {e}[/bold red]")
            sys.exit(1)


if __name__ == "__main__":
    main()
