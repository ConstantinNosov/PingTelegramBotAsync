import asyncio
import yaml

class AsyncPingTester:
    def __init__(self, hosts_file):
        self.hosts_file = hosts_file
        # Сохранение полных данных о хостах
        self.hosts = self.read_hosts()

    def read_hosts(self):
        """Читает список хостов и их описания из YAML файла."""
        with open(self.hosts_file, 'r') as file:
            data = yaml.safe_load(file)
        # Сохранение хостов с описаниями
        hosts = []
        if 'hosts' in data:
            for item in data['hosts']:
                if 'host' in item and 'description' in item:
                    # Сохранение словаря для каждого хоста
                    hosts.append({'host': item['host'], 'description': item['description']})
        return hosts

    async def ping_host(self, host):
        """Асинхронно пингует указанный хост."""
        process = await asyncio.create_subprocess_exec(
            'ping', '-c', '3', host,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return process.returncode == 0  # True, если хост достижим

    async def ping_test(self):
        """Асинхронно пингует все хосты из списка и возвращает результаты с описаниями."""
        tasks = []
        for host_info in self.hosts:
            task = asyncio.create_task(self.ping_host(host_info['host']))
            tasks.append((task, host_info))

        results = {}
        for task, host_info in tasks:
            reachable = await task
            # Включение описания в результаты
            results[host_info['host']] = {'reachable': reachable, 'description': host_info['description']}
        return results

    async def get_unreachable_hosts(self):
        """Асинхронно возвращает список недоступных хостов с их описаниями после пинг-теста."""
        results = await self.ping_test()
        # Включение описаний в вывод
        unreachable_hosts = [{'host': host, 'description': info['description']}
                             for host, info in results.items() if not info['reachable']]
        return unreachable_hosts
