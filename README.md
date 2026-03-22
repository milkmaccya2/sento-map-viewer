# sento-map-viewer

13年分のGoogle Mapsタイムラインから抽出した銭湯・サウナの訪問記録を地図上に可視化するWebアプリ。

https://milkmaccya2.github.io/sento-map-viewer/

## 機能

- **マーカー表示** — 訪問回数に応じてマーカーサイズが変化。クリックで施設名・訪問回数・年別推移・公式サイトリンクを表示
- **ヒートマップ** — 訪問頻度をヒートマップで可視化
- **年別フィルター** — 年ごとに絞り込み。統計・ランキング・地図が連動
- **ランキングサイドバー** — 訪問回数順のリスト。クリックで地図がフライ

## データの準備

訪問データは [google-maps-timeline-sento](https://github.com/milkmaccya2/google-maps-timeline-sento) で生成したCSVを使用。

```bash
python3 prepare_data.py
```

`sento-visits.csv` と `sento-ranking-with-urls.csv` を結合して `public/sento-data.json` を生成する。

## 技術スタック

- HTML / CSS / JavaScript（ビルドツール不要）
- [Leaflet](https://leafletjs.com/) + [Leaflet.heat](https://github.com/Leaflet/Leaflet.heat)
- [CARTO Dark Matter](https://carto.com/basemaps/) タイル
- GitHub Pages でホスティング

## 関連

- [銭湯ランキング記事（Qiita）](https://qiita.com/milkmaccya2/items/1e1ef669b9b5c5d78367)
- [データ抽出スクリプト](https://github.com/milkmaccya2/google-maps-timeline-sento)
