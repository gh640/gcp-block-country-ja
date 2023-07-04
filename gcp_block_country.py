"""Google Cloud Platform で特定の国からのアクセスをブロックするルールを作成するためのスクリプト"""

import argparse
import subprocess
import sys
from math import ceil
from pathlib import Path

CHUNK_SIZE = 256
# サポート対象の国の一覧
# キー: 国コード / バリュー: ルールのプリフィックス
COUNTRIES = {
    'cn': 'block-china-',
    'ru': 'block-russia-',
    'au': 'block-australia-',
}


def main():
    """メイン関数"""
    args = get_args()
    dry_run = args.dry_run
    country_code = args.country_code
    gcp_project = args.gcp_project

    addresses = get_addresses(country_code)
    total_count = len(addresses)
    print(f'Total addresses: {total_count}')
    print(f'Total rules being created: {ceil(total_count / CHUNK_SIZE)}')

    name_prefix = COUNTRIES[country_code]
    create_rules(name_prefix, addresses, dry_run=dry_run, gcp_project=gcp_project)


def get_args():
    """コマンドライン引数を取得する"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true', help='ドライラン')
    parser.add_argument('--country-code', required=True, help='国コード')
    parser.add_argument('--gcp-project', required=True, help='GCP プロジェクト')

    return parser.parse_args()


def create_rules(
    name_prefix: str, addresses: list[str], *, dry_run: bool, gcp_project: str
):
    """ファイヤウォールルールを複数件まとめて作成する"""
    n = 0
    while True:
        start = n * CHUNK_SIZE
        stop = start + CHUNK_SIZE

        chunk_addresses = addresses[start:stop]
        if not chunk_addresses:
            break

        name = f'{name_prefix}{n}'
        create_rule(name, chunk_addresses, dry_run=dry_run, gcp_project=gcp_project)
        n += 1


def create_rule(name: str, addresses: list[str], *, dry_run: bool, gcp_project: str):
    """ファイヤウォールルールを 1 件作成する"""
    args = [
        'gcloud',
        'compute',
        'firewall-rules',
        'create',
        name,
        f'--project={gcp_project}',
        '--action=DENY',
        '--rules=ALL',
        '--direction=INGRESS',
        '--priority=10',
        '--no-enable-logging',
        f'--source-ranges={",".join(addresses)}',
    ]
    if dry_run:
        print('Run:', ' '.join(args))
        return

    # Windows では `shell=True` が必要
    kwargs = {'check': True}
    if sys.platform == 'win32':
        kwargs['shell'] = True

    return subprocess.run(args, **kwargs)


def get_addresses(country_code: str) -> list[str]:
    """アドレス一覧を取得する"""

    def is_valid(line: str):
        return line.strip() and not line.startswith('#')

    content = Path(f'./{country_code}.txt').read_text()
    addresses = [l for l in content.splitlines() if is_valid(l)]

    return addresses


if __name__ == '__main__':
    main()
