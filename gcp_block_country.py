"""Google Cloud Platform で特定の国からのアクセスをブロックするルールを作成するためのスクリプト"""

import argparse
import subprocess

CHUNK_SIZE = 256
# サポート対象の国の一覧
# キー: 国コード / バリュー: ルールのプリフィックス
COUNTRIES = {
    'cn': 'block-china-',
    'ru': 'block-russia-',
}


def main():
    """メイン関数"""
    args = get_args()
    dry_run = args.dry_run
    country_code = args.country_code

    addresses = get_addresses(country_code)

    name_prefix = COUNTRIES[country_code]
    create_rules(name_prefix, addresses, dry_run=dry_run)


def get_args():
    """コマンドライン引数を取得する"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true', help='ドライラン')
    parser.add_argument('--country-code', required=True, help='国コード')

    return parser.parse_args()


def create_rules(name_prefix, addresses, *, dry_run):
    """ファイヤウォールルールを複数件まとめて作成する"""
    n = 0
    while True:
        start = n * CHUNK_SIZE
        stop = start + CHUNK_SIZE

        chunk_addresses = addresses[start:stop]
        if not chunk_addresses:
            break

        name = '{}{}'.format(name_prefix, n)
        create_rule(name, chunk_addresses, dry_run=dry_run)
        n += 1


def create_rule(name, addresses, *, dry_run):
    """ファイヤウォールルールを 1 件作成する"""
    args = [
        'gcloud',
        'compute',
        'firewall-rules',
        'create',
        name,
        '--action=DENY',
        '--rules=ALL',
        '--direction=INGRESS',
        '--priority=10',
        '--no-enable-logging',
        '--source-ranges={}'.format(','.join(addresses)),
    ]
    if dry_run:
        print('Run:', ' '.join(args))
        return

    return subprocess.run(args, check=True)


def get_addresses(country_code):
    """アドレス一覧を取得する"""

    def is_valid(line):
        return line.strip() and not line.startswith('#')

    with open('./{}.txt'.format(country_code)) as f:
        addresses = [l.strip() for l in f.readlines() if is_valid(l)]

    return addresses


if __name__ == '__main__':
    main()
