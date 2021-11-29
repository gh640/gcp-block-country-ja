# `gcp_block_country.py`

Google Cloud Platform で特定の国からのアクセスをブロックするルールを作成するためのサンプルスクリプトです。
あくまでもサンプルです。

## 必須

- Python 3
- [`gcloud` コマンドラインツール](https://cloud.google.com/sdk)

## 使い方

`git clone` でスクリプトをダウンロードします。

```bash
git clone https://github.com/gh640/gcp-block-country-ja
```

対象とする IP アドレスの範囲をリストしたテキストファイルを用意します。

```bash
curl -O https://ipv4.fetus.jp/cn.txt
```

ファイルの中身のサンプル:

```text
#
# [cn] 中華人民共和国 (China)
#  https://ipv4.fetus.jp/cn.txt
#  出力日時: xxx
#

1.0.1.0/24
1.0.2.0/23
1.0.8.0/21
1.0.32.0/19
```

GCP プロジェクトと国コードを指定して dry run モードで実行します。

```bash
python gcp_block_country.py --gcp-project my-project --country-code cn --dry-run
```

問題がなさそうであれば dry run オプションを外して実行します。

```bash
python gcp_block_country.py --gcp-project my-project --country-code cn
```

```text
$ python gcp_block_country.py --help
usage: gcp_block_country.py [-h] [--dry-run] --country-code COUNTRY_CODE --gcp-project GCP_PROJECT

Google Cloud Platform で特定の国からのアクセスをブロックするルールを作成するためのスクリプト

optional arguments:
  -h, --help            show this help message and exit
  --dry-run             ドライラン
  --country-code COUNTRY_CODE
                        国コード
  --gcp-project GCP_PROJECT
                        GCP プロジェクト
usage: gcp_block_country.py [-h] [--dry-run] --country-code COUNTRY_CODE
```

### 有効な国コード

現在、以下の国コードが利用可能です。

- `cn`: 中国
- `ru`: ロシア
- `au`: オーストラリア

## 説明記事

- [Google Cloud Platform で特定の国からのアクセスをブロックする方法 | gotohayato.com](https://gotohayato.com/content/520/)

## 関連リポジトリ

- [GitHub - gh640/gcp-allow-only-japan-ja](https://github.com/gh640/gcp-allow-only-japan-ja)

## 参考

- [VPC firewall rules overview  |  Google Cloud](https://cloud.google.com/vpc/docs/firewalls)
- [Using firewall rules  |  VPC  |  Google Cloud](https://cloud.google.com/vpc/docs/using-firewalls)
- [`gcloud compute firewall-rules create`  |  Cloud SDK Documentation](https://cloud.google.com/sdk/gcloud/reference/compute/firewall-rules/create)
- [ipv4.fetus.jp : 国/地域別IPアドレス(IPv4アドレス)割り当て一覧](https://ipv4.fetus.jp/)
