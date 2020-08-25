# `gcp_block_country.py`

Google Cloud Platform で特定の国からのアクセスをブロックするルールを作成するためのサンプルスクリプトです。
あくまでもサンプルです。

## 使い方

`git clone` でスクリプトをダウンロードします。

```bash
git clone
```

対象とする IP アドレスの範囲をリストしたテキストファイルを用意します。

```bash
curl -O https://ipv4.fetus.jp/cn.txt
```

国コードを指定して dry run モードで実行します。

```bash
python gcp_block_country.py --country-code cn --dry-run
```

問題がなさそうであれば dry run を外して実行します。

```bash
python gcp_block_country.py --country-code cn
```

```text
python gcp_block_country.py --help
usage: gcp_block_country.py [-h] [--dry-run] --country-code COUNTRY_CODE

Google Cloud Platform で特定の国からのアクセスをブロックするルールを作成するためのスクリプト

optional arguments:
  -h, --help            show this help message and exit
  --dry-run             ドライラン
  --country-code COUNTRY_CODE
                        国コード
```

## 参考

- [VPC firewall rules overview  |  Google Cloud](https://cloud.google.com/vpc/docs/firewalls)
- [Using firewall rules  |  VPC  |  Google Cloud](https://cloud.google.com/vpc/docs/using-firewalls)
- [`gcloud compute firewall-rules create`  |  Cloud SDK Documentation](https://cloud.google.com/sdk/gcloud/reference/compute/firewall-rules/create)
- [ipv4.fetus.jp : 国/地域別IPアドレス(IPv4アドレス)割り当て一覧](https://ipv4.fetus.jp/)
